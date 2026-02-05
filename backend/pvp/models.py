from django.db import models
from django.contrib.auth.models import User

from tasks.models import Task 

class QuizRoom(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='p1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='p2')
    
    
    tasks = models.ManyToManyField(Task, related_name='rooms')
    
    current_task_index = models.IntegerField(default=0)
    score_p1 = models.IntegerField(default=0)
    score_p2 = models.IntegerField(default=0)
    
    p1_submitted = models.BooleanField(default=False)
    p2_submitted = models.BooleanField(default=False)
    
    subject = models.CharField(max_length=100, choices=Task.SUBJECTS)
    difficulty = models.CharField(max_length=20, choices=Task.DIFFICULTY_CHOICES)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room_id} | {self.subject}"