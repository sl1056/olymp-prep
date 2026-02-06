import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth import get_user_model

# Импорты из ваших файлов
from .models import Match
from .serializers import MatchSerializer
from elo import calculate_elo

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
            answer_text = content.get('answer')
            if answer_text:
                await self.handle_answer_submission(answer_text)

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

    # --- Database Sync Methods ---

    @database_sync_to_async
    def check_participation(self, match_id, user):
        try:
            match = Match.objects.get(id=match_id)
            return match.player1 == user or match.player2 == user
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

        # Проверяем, ответили ли оба
        p1_done = match.player1_submitted_at is not None
        p2_done = match.player2_submitted_at is not None
        
        return (p1_done and p2_done), p1_done, p2_done

    @database_sync_to_async
    def finalize_match_logic(self, match_id):
        match = Match.objects.select_related('player1', 'player1__profile', 'player2', 'player2__profile').get(id=match_id)
        
        # Логика результата для ELO (1=победа P1, 0=победа P2, 0.5=ничья)
        # Приоритет: Правильность -> Время (если нужно) -> Ничья
        
        result_val = 0.5
        
        p1_win = False
        p2_win = False
        is_draw = False

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