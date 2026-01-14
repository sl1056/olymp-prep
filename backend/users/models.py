from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    rating = models.IntegerField(default=1000)
    solved_tasks = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Профиль пользователя {self.user.username}'
