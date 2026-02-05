from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task

class Match(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Ожидание второго игрока'),
        ('active', 'Игра идёт'),
        ('finished', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]

    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_player2', null=True,
                                blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    player1_answer = models.TextField(blank=True)
    player2_answer = models.TextField(blank=True)

    player1_submitted_at = models.DateTimeField(null=True, blank=True)
    player2_submitted_at = models.DateTimeField(null=True, blank=True)

    player1_correct = models.BooleanField(default=False)
    player2_correct = models.BooleanField(default=False)

    def __str__(self):
        p2 = self.player2.username if self.player2 else "—"
        return f"Match {self.id}: {self.player1.username} vs {p2}"