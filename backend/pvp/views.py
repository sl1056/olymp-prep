import uuid
from django.shortcuts import render
from .models import QuizRoom, Question
from django.db.models import Q

def find_or_create_room(user):
    
    room = QuizRoom.objects.filter(player2__isnull=True, is_active=True).exclude(player1=user).first()
    
    if room:
        room.player2 = user
        room.save()
    else:
        room = QuizRoom.objects.create(
            room_id=str(uuid.uuid4())[:8],
            player1=user
        )
        random_questions = Question.objects.order_by('?')[:5]
        room.questions.set(random_questions)
    
    return room