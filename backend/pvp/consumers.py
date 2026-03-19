import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.db import transaction

from .models import Match
from .elo import calculate_elo

logger = logging.getLogger(__name__)


class MatchConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.group_name = f'match_{self.match_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        is_participant = await self.check_participation(self.match_id, self.user.id)
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()


        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'player_joined',
                'user_id': self.user.id,
                'username': self.user.username
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )



    async def receive_json(self, content):
        command = content.get('command')

        if command == 'submit_answer':
            answer_text = content.get('answer', '').strip()
            if answer_text:
                await self.handle_answer_submission(answer_text)



    async def player_joined(self, event):
        await self.send_json({
            'type': 'player_joined',
            'user_id': event['user_id'],
            'username': event['username']
        })

    async def answer_submitted(self, event):
        await self.send_json({
            'type': 'opponent_submitted',
            'user_id': event['user_id']
        })

    async def match_finished(self, event):
        await self.send_json({
            'type': 'game_over',
            'results': event['data']
        })

    async def question_changed(self, event):
        await self.send_json({
            'type': 'next_question',
            'data': event['data']
        })



    async def handle_answer_submission(self, answer_text):
        match_status = await self.get_match_status()
        if match_status in ['finished', 'cancelled']:
            await self.send_json({'error': 'Матч уже завершён'})
            return

        submission_result = await self.save_answer_to_db(answer_text)
        if not submission_result['accepted']:
            await self.send_json({'error': submission_result['reason']})
            return

        both_submitted = submission_result['both_submitted']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'answer_submitted',
                'user_id': self.user.id
            }
        )

        if both_submitted:
            try:
                next_question_data = await self.advance_to_next_question(self.match_id)
            except Exception:
                logger.exception("Failed to advance PvP match %s", self.match_id)
                await self.send_json({'error': 'Ошибка перехода к следующему вопросу.'})
                return

            if next_question_data:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'question_changed',
                        'data': next_question_data
                    }
                )
                return

            try:
                result_data = await self.finalize_match_logic(self.match_id)
            except Exception:
                logger.exception("Failed to finalize PvP match %s", self.match_id)
                await self.send_json({'error': 'Ошибка завершения матча. Попробуйте снова.'})
                return
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'match_finished',
                    'data': result_data
                }
            )

    @database_sync_to_async
    def check_participation(self, match_id, user_id):
        return self._check_participation(match_id, user_id)

    def _check_participation(self, match_id, user_id):
        try:
            match = Match.objects.get(id=match_id)
            return bool(match.player1_id == user_id or match.player2_id == user_id)
        except Match.DoesNotExist:
            return False

    @database_sync_to_async
    def get_match_status(self):
        try:
            match = Match.objects.get(id=self.match_id)
            return match.status
        except Match.DoesNotExist:
            return 'cancelled'

    @database_sync_to_async
    def save_answer_to_db(self, answer):
        return self._save_answer_to_db(answer)

    def _save_answer_to_db(self, answer):
        with transaction.atomic():
            match = Match.objects.select_for_update().select_related('task').get(id=self.match_id)

            if match.status != 'active' or not match.player2_id:
                return {
                    'accepted': False,
                    'both_submitted': False,
                    'reason': 'Матч ещё не готов к ответам',
                }

            is_correct = answer.strip().casefold() == match.task.correct_answer.strip().casefold()
            now = timezone.now()

            if match.player1_id == self.user.id:
                if match.player1_submitted_at:
                    return {
                        'accepted': False,
                        'both_submitted': False,
                        'reason': 'Ответ уже отправлен',
                    }
                match.player1_answer = answer
                match.player1_submitted_at = now
                match.player1_correct = is_correct
                if is_correct:
                    match.player1_score = int(match.player1_score or 0) + 1
            elif match.player2_id == self.user.id:
                if match.player2_submitted_at:
                    return {
                        'accepted': False,
                        'both_submitted': False,
                        'reason': 'Ответ уже отправлен',
                    }
                match.player2_answer = answer
                match.player2_submitted_at = now
                match.player2_correct = is_correct
                if is_correct:
                    match.player2_score = int(match.player2_score or 0) + 1
            else:
                return {
                    'accepted': False,
                    'both_submitted': False,
                    'reason': 'Вы не участник матча',
                }

            match.save(update_fields=[
                'player1_answer',
                'player2_answer',
                'player1_submitted_at',
                'player2_submitted_at',
                'player1_correct',
                'player2_correct',
                'player1_score',
                'player2_score',
            ])

            return {
                'accepted': True,
                'both_submitted': bool(match.player1_submitted_at and match.player2_submitted_at),
                'reason': None,
            }

    @database_sync_to_async
    def finalize_match_logic(self, match_id):
        return self._finalize_match_logic(match_id)

    @database_sync_to_async
    def advance_to_next_question(self, match_id):
        return self._advance_to_next_question(match_id)

    def _advance_to_next_question(self, match_id):
        with transaction.atomic():
            match = Match.objects.select_for_update().select_related('task').get(id=match_id)

            total_questions = max(1, int(match.questions_count or 1))
            question_task_ids = match.question_task_ids if isinstance(match.question_task_ids, list) else []

            if not question_task_ids and match.task_id:
                question_task_ids = [match.task_id]

            if match.current_question_index >= total_questions:
                return None

            next_question_index = match.current_question_index + 1
            if len(question_task_ids) < next_question_index:
                return None

            next_task_id = int(question_task_ids[next_question_index - 1])
            match.task_id = next_task_id
            match.current_question_index = next_question_index
            match.question_task_ids = question_task_ids
            match.questions_count = total_questions

            match.player1_answer = ''
            match.player2_answer = ''
            match.player1_submitted_at = None
            match.player2_submitted_at = None
            match.player1_correct = False
            match.player2_correct = False

            match.save(update_fields=[
                'task',
                'current_question_index',
                'question_task_ids',
                'questions_count',
                'player1_answer',
                'player2_answer',
                'player1_submitted_at',
                'player2_submitted_at',
                'player1_correct',
                'player2_correct',
            ])

            match = Match.objects.select_related('task').get(id=match.id)
            return {
                'match_id': match.id,
                'task_text': match.task.text,
                'current_question_index': match.current_question_index,
                'questions_count': match.questions_count,
                'player1_score': match.player1_score,
                'player2_score': match.player2_score,
            }

    def _finalize_match_logic(self, match_id):
        with transaction.atomic():
            # Lock only the match row first. Doing select_for_update with
            # nullable joins (player2/profile) triggers Postgres error:
            # "FOR UPDATE cannot be applied to the nullable side of an outer join".
            locked_match = Match.objects.select_for_update().get(id=match_id)
            match = Match.objects.select_related(
                'player1__profile',
                'player2__profile',
                'task'
            ).get(id=locked_match.id)

            if match.status == 'finished':
                if match.player1_score > match.player2_score:
                    winner = 'player1'
                elif match.player2_score > match.player1_score:
                    winner = 'player2'
                else:
                    winner = 'draw'

                return {
                    'match_id': match.id,
                    'winner': winner,
                    'player1_username': match.player1.username,
                    'player2_username': match.player2.username,
                    'player1_new_rating': match.player1.profile.rating,
                    'player2_new_rating': match.player2.profile.rating,
                    'player1_correct': match.player1_correct,
                    'player2_correct': match.player2_correct,
                    'player1_score': match.player1_score,
                    'player2_score': match.player2_score,
                    'total_questions': max(1, int(match.questions_count or 1)),
                    'correct_answer': match.task.correct_answer,
                }

            if match.player1_score > match.player2_score:
                result = 1.0
            elif match.player2_score > match.player1_score:
                result = 0.0
            else:
                result = 0.5

            p1_rating = match.player1.profile.rating
            p2_rating = match.player2.profile.rating

            new_p1, new_p2 = calculate_elo(p1_rating, p2_rating, result)
            solved_delta = max(1, int(match.questions_count or 1))

            match.player1.profile.rating = new_p1
            match.player2.profile.rating = new_p2
            match.player1.profile.solved_tasks += solved_delta
            match.player2.profile.solved_tasks += solved_delta
            match.player1.profile.correct_answers += int(match.player1_score or 0)
            match.player2.profile.correct_answers += int(match.player2_score or 0)

            match.player1.profile.save()
            match.player2.profile.save()

            match.status = 'finished'
            match.finished_at = timezone.now()
            match.save(update_fields=['status', 'finished_at'])

            return {
                'match_id': match.id,
                'winner': (
                    'player1' if result == 1.0 else
                    'player2' if result == 0.0 else
                    'draw'
                ),
                'player1_username': match.player1.username,
                'player2_username': match.player2.username,
                'player1_new_rating': new_p1,
                'player2_new_rating': new_p2,
                'player1_correct': match.player1_correct,
                'player2_correct': match.player2_correct,
                'player1_score': match.player1_score,
                'player2_score': match.player2_score,
                'total_questions': max(1, int(match.questions_count or 1)),
                'correct_answer': match.task.correct_answer,
            }
