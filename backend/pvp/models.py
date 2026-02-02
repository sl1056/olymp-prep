from django.db import models
from django.contrib.auth.models import User

class QuizRoom(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='p1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='p2')
    current_question_index = models.IntegerField(default=0)
    score_p1 = models.IntegerField(default=0)
    score_p2 = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)