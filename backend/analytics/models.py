from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task


class TaskAttempt(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attempts')
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    subject = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=20)

    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['user', '-submitted_at']),
            models.Index(fields=['user', 'subject']),
            models.Index(fields=['user', 'difficulty']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.task.subject} ({'✓' if self.is_correct else '✗'})"