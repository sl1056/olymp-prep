import json
from datetime import timedelta
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth import get_user_model

# Импорты из ваших файлов
from .models import Match
<<<<<<< Updated upstream
from .serializers import MatchSerializer
from elo import calculate_elo
=======
from .elo import calculate_elo
from users.models import Profile
from tasks.models import Task
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

User = get_user_model()

class MatchConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = f'match_{self.match_id}'
        self.user = self.scope['user']

        # Проверка авторизации
        if not self.user.is_authenticated:
            await self.close()
            return

        # Проверка доступа к матчу
        is_participant = await self.check_participation(self.match_id, self.user)
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Отправляем текущее состояние матча при подключении
        match_data = await self.get_match_state()
        await self.send_json({
            'type': 'match_state',
            'data': match_data
        })
        
        # Уведомляем оппонента (группу) о подключении игрока
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_update',
                'message': f'Игрок {self.user.username} подключился'
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Обработка сообщений от WebSocket клиента
    async def receive_json(self, content):
        command = content.get('command')
        
        if command == 'submit_answer':
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            answer_text = content.get('answer')
            if answer_text:
                await self.handle_answer_submission(answer_text)
=======
            answer_text = content.get('answer', '')
            await self.handle_answer_submission(answer_text)
>>>>>>> Stashed changes
=======
            answer_text = content.get('answer', '')
            await self.handle_answer_submission(answer_text)
>>>>>>> Stashed changes
=======
            answer_text = content.get('answer', '')
            await self.handle_answer_submission(answer_text)
>>>>>>> Stashed changes
=======
            answer_text = content.get('answer', '')
            await self.handle_answer_submission(answer_text)
>>>>>>> Stashed changes

    # Обработка отправки ответа
    async def handle_answer_submission(self, answer_text):
        match = await self.get_match_instance()
        
        # Если матч уже завершен или отменен, игнорируем
        if match.status in ['finished', 'cancelled']:
            await self.send_json({'error': 'Матч уже завершен'})
            return

        # Сохраняем ответ
        match_finished, p1_ready, p2_ready = await self.save_answer_to_db(match, answer_text)

        # Уведомляем игроков, что один из них ответил (скрывая ответ)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'answer_submitted',
                'user_id': self.user.id
            }
        )

        # Если оба ответили, завершаем матч и считаем ELO
        if match_finished:
            elo_results = await self.finalize_match_logic(match.id)
            
            # Рассылаем финальный результат
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'match_finished',
                    'data': elo_results
                }
            )

    # --- Handlers для group_send ---

    async def player_update(self, event):
        await self.send_json({
            'type': 'player_update',
            'message': event['message']
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

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    # --- Database Sync Methods ---
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    async def next_question(self, event):
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

        # Confirm that the answer has been stored successfully.
        await self.send_json({'type': 'answer_accepted'})

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'answer_submitted',
                'user_id': self.user.id
            }
        )

        if both_submitted:
            result_data = await self.finalize_match_logic(self.match_id)
            event_type = result_data.get('event')

            if event_type == 'next_question':
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'next_question',
                        'data': result_data
                    }
                )
            elif event_type == 'finished':
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'match_finished',
                        'data': result_data
                    }
                )
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

    @database_sync_to_async
    def check_participation(self, match_id, user):
        try:
            match = Match.objects.get(id=match_id)
<<<<<<< Updated upstream
            return match.player1 == user or match.player2 == user
=======
            if match.player1_id == user_id:
                return True

            if match.player2_id == user_id:
                return True
            if not match.player2_id:
                return match.player1_id == user_id

            return False
>>>>>>> Stashed changes
        except Match.DoesNotExist:
            return False

    @database_sync_to_async
    def get_match_state(self):
        try:
            match = Match.objects.get(id=self.match_id)
            return MatchSerializer(match).data
        except Match.DoesNotExist:
            return {}

    @database_sync_to_async
    def get_match_instance(self):
        return Match.objects.select_related('task', 'player1', 'player2').get(id=self.match_id)

    @database_sync_to_async
    def save_answer_to_db(self, match, answer):
        is_correct = (answer.strip().lower() == match.task.correct_answer.strip().lower())
        now = timezone.now()

        if match.player1 == self.user:
            match.player1_answer = answer
            match.player1_submitted_at = now
            match.player1_correct = is_correct
        elif match.player2 == self.user:
            match.player2_answer = answer
            match.player2_submitted_at = now
            match.player2_correct = is_correct
        
        match.save()

<<<<<<< Updated upstream
        # Проверяем, ответили ли оба
        p1_done = match.player1_submitted_at is not None
        p2_done = match.player2_submitted_at is not None
        
        return (p1_done and p2_done), p1_done, p2_done
=======
            now = timezone.now()
            answer_text = (answer or '').strip()

            if self._time_is_expired(match, now) and answer_text:
                return {
                    'accepted': False,
                    'both_submitted': False,
                    'reason': 'Время на вопрос истекло',
                }

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
            now = timezone.now()
            answer_text = (answer or '').strip()

            if self._time_is_expired(match, now) and answer_text:
                return {
                    'accepted': False,
                    'both_submitted': False,
                    'reason': 'Время на вопрос истекло',
                }

<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
            is_correct = answer_text.casefold() == match.task.correct_answer.strip().casefold()

            if match.player1_id == self.user.id:
                if match.player1_submitted_at:
                    return {
                        'accepted': False,
                        'both_submitted': False,
                        'reason': 'Ответ уже отправлен',
                    }
                match.player1_answer = answer_text
                match.player1_submitted_at = now
                match.player1_correct = is_correct
            elif match.player2_id == self.user.id:
                if match.player2_submitted_at:
                    return {
                        'accepted': False,
                        'both_submitted': False,
                        'reason': 'Ответ уже отправлен',
                    }
                match.player2_answer = answer_text
                match.player2_submitted_at = now
                match.player2_correct = is_correct
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
            ])

            return {
                'accepted': True,
                'both_submitted': bool(match.player1_submitted_at and match.player2_submitted_at),
                'reason': None,
            }
>>>>>>> Stashed changes

    @database_sync_to_async
    def finalize_match_logic(self, match_id):
        match = Match.objects.select_related('player1', 'player1__profile', 'player2', 'player2__profile').get(id=match_id)
        
        # Логика результата для ELO (1=победа P1, 0=победа P2, 0.5=ничья)
        # Приоритет: Правильность -> Время (если нужно) -> Ничья
        
        result_val = 0.5
        
        p1_win = False
        p2_win = False
        is_draw = False

<<<<<<< Updated upstream
        if match.player1_correct and not match.player2_correct:
            result_val = 1.0
            p1_win = True
        elif not match.player1_correct and match.player2_correct:
            result_val = 0.0
            p2_win = True
        elif match.player1_correct and match.player2_correct:
            # Оба ответили верно - ничья (или можно сравнивать время submitted_at)
            result_val = 0.5
            is_draw = True
        else:
            # Оба ответили неверно
            result_val = 0.5
            is_draw = True

        # Обновляем ELO
        # Предполагаем наличие profile с полем elo (на основе provided views-tasks.py)
        # Если поля elo нет, нужно добавить миграцию или обработку ошибок, 
        # но по условию менять файлы нельзя, рассчитываем что модель готова.
        
        p1_rating = match.player1.profile.elo
        p2_rating = match.player2.profile.elo

        new_p1_rating, new_p2_rating = calculate_elo(p1_rating, p2_rating, result_val)

        # Сохраняем новые рейтинги
        match.player1.profile.elo = new_p1_rating
        match.player1.profile.save()
        
        match.player2.profile.elo = new_p2_rating
        match.player2.profile.save()

        # Обновляем статус матча
        match.status = 'finished'
        match.finished_at = timezone.now()
        match.save()
        
        # Обновляем статистику задач (solved/correct)
        # P1
        match.player1.profile.solved_tasks += 1
        if match.player1_correct:
             match.player1.profile.correct_answers += 1
        match.player1.profile.save()
        
        # P2
        match.player2.profile.solved_tasks += 1
        if match.player2_correct:
             match.player2.profile.correct_answers += 1
        match.player2.profile.save()

        return {
            'match_id': match.id,
            'winner': 'player1' if p1_win else ('player2' if p2_win else 'draw'),
            'player1_username': match.player1.username,
            'player2_username': match.player2.username,
            'player1_elo_change': new_p1_rating - p1_rating,
            'player2_elo_change': new_p2_rating - p2_rating,
            'player1_new_elo': new_p1_rating,
            'player2_new_elo': new_p2_rating,
            'correct_answer': match.task.correct_answer,
            'player1_answer': match.player1_answer,
            'player2_answer': match.player2_answer,
            'player1_correct': match.player1_correct,
            'player2_correct': match.player2_correct
        }
=======
    def _time_is_expired(self, match, now):
        if (
            not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return False

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        return now >= deadline

    def _time_left_seconds(self, match):
        if (
            not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return None

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        return max(0, int((deadline - timezone.now()).total_seconds()))

    def _winner_by_score(self, match):
        if match.player1_score > match.player2_score:
            return 'player1'
        if match.player2_score > match.player1_score:
            return 'player2'
        return 'draw'

    def _build_finished_payload(self, match, p1_rating, p2_rating):
        return {
            'event': 'finished',
            'match_id': match.id,
            'winner': self._winner_by_score(match),
            'player1_username': match.player1.username,
            'player2_username': match.player2.username if match.player2 else None,
            'player1_new_rating': p1_rating,
            'player2_new_rating': p2_rating,
            'player1_score': match.player1_score,
            'player2_score': match.player2_score,
            'total_questions': match.questions_count,
            'player1_correct': match.player1_correct,
            'player2_correct': match.player2_correct,
            'correct_answer': match.task.correct_answer,
        }

    def _time_is_expired(self, match, now):
        if (
            not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return False

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        return now >= deadline

    def _time_left_seconds(self, match):
        if (
            not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return None

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        return max(0, int((deadline - timezone.now()).total_seconds()))

    def _winner_by_score(self, match):
        if match.player1_score > match.player2_score:
            return 'player1'
        if match.player2_score > match.player1_score:
            return 'player2'
        return 'draw'

    def _build_finished_payload(self, match, p1_rating, p2_rating):
        return {
            'event': 'finished',
            'match_id': match.id,
            'winner': self._winner_by_score(match),
            'player1_username': match.player1.username,
            'player2_username': match.player2.username if match.player2 else None,
            'player1_new_rating': p1_rating,
            'player2_new_rating': p2_rating,
            'player1_score': match.player1_score,
            'player2_score': match.player2_score,
            'total_questions': match.questions_count,
            'player1_correct': match.player1_correct,
            'player2_correct': match.player2_correct,
            'correct_answer': match.task.correct_answer,
        }

    def _time_is_expired(self, match, now):
        if (
            not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return False

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        return now >= deadline

    def _time_left_seconds(self, match):
        if (
            not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return None

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        return max(0, int((deadline - timezone.now()).total_seconds()))

    def _winner_by_score(self, match):
        if match.player1_score > match.player2_score:
            return 'player1'
        if match.player2_score > match.player1_score:
            return 'player2'
        return 'draw'

    def _build_finished_payload(self, match, p1_rating, p2_rating):
        return {
            'event': 'finished',
            'match_id': match.id,
            'winner': self._winner_by_score(match),
            'player1_username': match.player1.username,
            'player2_username': match.player2.username if match.player2 else None,
            'player1_new_rating': p1_rating,
            'player2_new_rating': p2_rating,
            'player1_score': match.player1_score,
            'player2_score': match.player2_score,
            'total_questions': match.questions_count,
            'player1_correct': match.player1_correct,
            'player2_correct': match.player2_correct,
            'correct_answer': match.task.correct_answer,
        }

    def _time_is_expired(self, match, now):
        if (
            not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return False

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        return now >= deadline

    def _time_left_seconds(self, match):
        if (
            not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return None

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        return max(0, int((deadline - timezone.now()).total_seconds()))

    def _winner_by_score(self, match):
        if match.player1_score > match.player2_score:
            return 'player1'
        if match.player2_score > match.player1_score:
            return 'player2'
        return 'draw'

    def _build_finished_payload(self, match, p1_rating, p2_rating):
        return {
            'event': 'finished',
            'match_id': match.id,
            'winner': self._winner_by_score(match),
            'player1_username': match.player1.username,
            'player2_username': match.player2.username if match.player2 else None,
            'player1_new_rating': p1_rating,
            'player2_new_rating': p2_rating,
            'player1_score': match.player1_score,
            'player2_score': match.player2_score,
            'total_questions': match.questions_count,
            'player1_correct': match.player1_correct,
            'player2_correct': match.player2_correct,
            'correct_answer': match.task.correct_answer,
        }

    def _finalize_match_logic(self, match_id):
        with transaction.atomic():
            # Do not join nullable player2 under FOR UPDATE (PostgreSQL limitation).
            match = Match.objects.select_for_update().select_related(
                'player1',
                'task'
            ).get(id=match_id)

            task_ids = list(match.question_task_ids or [match.task_id])
            if not task_ids:
                task_ids = [match.task_id]
            if match.questions_count < 1:
                match.questions_count = 1
            if len(task_ids) < match.questions_count:
                task_ids.extend([task_ids[-1]] * (match.questions_count - len(task_ids)))
                match.question_task_ids = task_ids
            if match.current_question_index < 1:
                match.current_question_index = 1

            if not match.player2_id:
                p1_profile, _ = Profile.objects.get_or_create(user_id=match.player1_id)
                return self._build_finished_payload(match, p1_profile.rating, None)

            Profile.objects.get_or_create(user_id=match.player1_id)
            Profile.objects.get_or_create(user_id=match.player2_id)
            profiles = Profile.objects.select_for_update().filter(
                user_id__in=[match.player1_id, match.player2_id]
            )
            profiles_map = {profile.user_id: profile for profile in profiles}

            p1_profile = profiles_map.get(match.player1_id)
            p2_profile = profiles_map.get(match.player2_id)

            if match.status == 'finished':
                return self._build_finished_payload(match, p1_profile.rating, p2_profile.rating)

            both_submitted = bool(match.player1_submitted_at and match.player2_submitted_at)
            if match.status != 'active' or not both_submitted:
                return {'event': 'pending'}

            if match.player1_correct:
                match.player1_score += 1
            if match.player2_correct:
                match.player2_score += 1

            has_next_question = match.current_question_index < match.questions_count
            if has_next_question:
                next_index = match.current_question_index + 1
                next_task_id = task_ids[next_index - 1]
                next_task = Task.objects.get(id=next_task_id)

                match.current_question_index = next_index
                match.task = next_task
                match.current_question_started_at = timezone.now() if match.timer_enabled else None
                match.player1_answer = ''
                match.player2_answer = ''
                match.player1_submitted_at = None
                match.player2_submitted_at = None
                match.player1_correct = False
                match.player2_correct = False
                match.save(update_fields=[
                    'questions_count',
                    'current_question_index',
                    'question_task_ids',
                    'task',
                    'current_question_started_at',
                    'player1_score',
                    'player2_score',
                    'player1_answer',
                    'player2_answer',
                    'player1_submitted_at',
                    'player2_submitted_at',
                    'player1_correct',
                    'player2_correct',
                ])

                return {
                    'event': 'next_question',
                    'match_id': match.id,
                    'task_text': next_task.text,
                    'current_question_index': match.current_question_index,
                    'questions_count': match.questions_count,
                    'player1_score': match.player1_score,
                    'player2_score': match.player2_score,
                    'timer_enabled': match.timer_enabled,
                    'time_limit_seconds': match.time_limit_seconds,
                    'time_left_seconds': self._time_left_seconds(match),
                    'hints_enabled': match.hints_enabled,
                    'task_hints': (next_task.hints or []) if match.hints_enabled else [],
                }

            if match.player1_score > match.player2_score:
                result = 1.0
            elif match.player2_score > match.player1_score:
                result = 0.0
            else:
                result = 0.5

            p1_rating = p1_profile.rating
            p2_rating = p2_profile.rating

            new_p1, new_p2 = calculate_elo(p1_rating, p2_rating, result)

            p1_profile.rating = new_p1
            p2_profile.rating = new_p2
            p1_profile.solved_tasks += match.questions_count
            p2_profile.solved_tasks += match.questions_count
            p1_profile.correct_answers += match.player1_score
            p2_profile.correct_answers += match.player2_score

            p1_profile.save(update_fields=['rating', 'solved_tasks', 'correct_answers'])
            p2_profile.save(update_fields=['rating', 'solved_tasks', 'correct_answers'])

            match.status = 'finished'
            match.finished_at = timezone.now()
            match.save(update_fields=[
                'questions_count',
                'player1_score',
                'player2_score',
                'status',
                'finished_at',
            ])

            return self._build_finished_payload(match, new_p1, new_p2)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
