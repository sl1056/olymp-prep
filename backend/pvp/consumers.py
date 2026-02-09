import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from .models import Match
from .elo import calculate_elo


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



    async def handle_answer_submission(self, answer_text):
        match_status = await self.get_match_status()
        if match_status in ['finished', 'cancelled']:
            await self.send_json({'error': 'Матч уже завершён'})
            return

        both_submitted = await self.save_answer_to_db(answer_text)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'answer_submitted',
                'user_id': self.user.id
            }
        )

        if both_submitted:
            result_data = await self.finalize_match_logic(self.match_id)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'match_finished',
                    'data': result_data
                }
            )



    @database_sync_to_async
    def check_participation(self, match_id, user_id):
        try:
            match = Match.objects.get(id=match_id)
            return match.player1_id == user_id or match.player2_id == user_id
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
        match = Match.objects.select_related('task').get(id=self.match_id)
        is_correct = answer.lower() == match.task.correct_answer.lower()
        now = timezone.now()

        if match.player1_id == self.user.id:
            match.player1_answer = answer
            match.player1_submitted_at = now
            match.player1_correct = is_correct
        elif match.player2_id == self.user.id:
            match.player2_answer = answer
            match.player2_submitted_at = now
            match.player2_correct = is_correct

        match.save()

        return bool(match.player1_submitted_at and match.player2_submitted_at)

    @database_sync_to_async
    def finalize_match_logic(self, match_id):
        from users.models import Profile

        match = Match.objects.select_related(
            'player1__profile',
            'player2__profile',
            'task'
        ).get(id=match_id)

        if match.player1_correct and not match.player2_correct:
            result = 1.0
        elif match.player2_correct and not match.player1_correct:
            result = 0.0
        else:
            result = 0.5

        p1_rating = match.player1.profile.rating
        p2_rating = match.player2.profile.rating

        new_p1, new_p2 = calculate_elo(p1_rating, p2_rating, result)

        match.player1.profile.rating = new_p1
        match.player2.profile.rating = new_p2
        match.player1.profile.solved_tasks += 1
        match.player2.profile.solved_tasks += 1

        if match.player1_correct:
            match.player1.profile.correct_answers += 1
        if match.player2_correct:
            match.player2.profile.correct_answers += 1

        match.player1.profile.save()
        match.player2.profile.save()

        match.status = 'finished'
        match.finished_at = timezone.now()
        match.save()

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
            'correct_answer': match.task.correct_answer,
        }
