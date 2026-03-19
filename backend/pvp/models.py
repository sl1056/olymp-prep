from django.db import models
from django.contrib.auth.models import User

<<<<<<< Updated upstream
from tasks.models import Task 
=======



class Match(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Ожидание второго игрока'),
        ('active', 'Игра идёт'),
        ('finished', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream

    def __str__(self):
        return f"Room {self.room_id} | {self.subject}"
=======
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    questions_count = models.PositiveSmallIntegerField(default=1)
    current_question_index = models.PositiveSmallIntegerField(default=1)
    question_task_ids = models.JSONField(default=list, blank=True)
    player1_score = models.PositiveSmallIntegerField(default=0)
    player2_score = models.PositiveSmallIntegerField(default=0)
    timer_enabled = models.BooleanField(default=True)
    hints_enabled = models.BooleanField(default=False)
    random_order = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    private_token = models.CharField(max_length=64, blank=True, default="")
    time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
    current_question_started_at = models.DateTimeField(null=True, blank=True)

    player1_answer = models.TextField(blank=True)
    player2_answer = models.TextField(blank=True)
    player1_submitted_at = models.DateTimeField(null=True, blank=True)
    player2_submitted_at = models.DateTimeField(null=True, blank=True)
    player1_correct = models.BooleanField(default=False)
    player2_correct = models.BooleanField(default=False)

    def __str__(self):
        p2 = self.player2.username if self.player2 else "—"
        return f"Match {self.id}: {self.player1.username} vs {p2}"
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
