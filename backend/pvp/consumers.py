import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import QuizRoom, Question

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'quiz_{self.room_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'submit_answer':
            answer = data.get('answer')
            user = self.scope['user']
            result = await self.process_answer(user, answer)
            
            # Рассылаем обновление всем в комнате
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'quiz_update',
                    'data': result
                }
            )

    @database_sync_to_async
    def process_answer(self, user, answer):
        room = QuizRoom.objects.get(room_id=self.room_id)
        questions = list(room.questions.all())
        current_q = questions[room.current_question_index]

        
        is_correct = current_q.answer.lower() == answer.lower()
        
        if user == room.player1:
            if not room.p1_ready:
                if is_correct: room.score_p1 += current_q.points
                room.p1_ready = True
        else:
            if not room.p2_ready:
                if is_correct: room.score_p2 += current_q.points
                room.p2_ready = True
        
        room.save()

        
        next_round = False
        if room.p1_ready and room.p2_ready:
            room.current_question_index += 1
            room.p1_ready = False
            room.p2_ready = False
            
            if room.current_question_index >= room.questions.count():
                room.is_active = False
                status = "finished"
            else:
                status = "next_question"
            room.save()
            next_round = True
        else:
            status = "waiting_opponent"

        return {
            "status": status,
            "score_p1": room.score_p1,
            "score_p2": room.score_p2,
            "current_index": room.current_question_index,
            "last_answer_user": user.username,
            "is_correct": is_correct
        }

    async def quiz_update(self, event):
        await self.send(text_data=json.dumps(event['data']))