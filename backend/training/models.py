from django.conf import settings
from django.db import models

# Create your models here.
from tasks.models import Task


class TrainingSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='training_sessions',
    )
    subject = models.CharField(max_length=100, choices=Task.SUBJECTS)
    total_tasks = models.PositiveIntegerField()
    task_ids = models.JSONField(default=list)
    current_position = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Тренировка #{self.id} ({self.user})"


class TrainingAnswer(models.Model):
    session = models.ForeignKey(
        TrainingSession,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='training_answers')
    user_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['answered_at']
        unique_together = ('session', 'task')

    def __str__(self):
        return f"{self.session_id}: {self.task_id}"