from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models import Q

from analytics.models import TaskAttempt
from pvp.models import Match


class Badge(models.Model):
    TYPE_CHOICES = [
        ('subject', 'По предмету'),
        ('total', 'Общие'),
        ('streak', 'Серии'),
        ('pvp', 'PvP'),
    ]

    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    icon = models.CharField(
        max_length=50,
        default='⭐',
        help_text='Эмодзи или короткий код иконки (напр. 🧮, 🧪, 💻)',
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='subject')
    condition_subject = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Предмет (например: 'math', 'phys') — только для type='subject'",
    )
    condition_min_solved = models.PositiveIntegerField(
        default=0,
        help_text='Мин. количество решённых задач',
    )
    condition_min_correct_ratio = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        help_text='Мин. % правильных ответов (0.0–1.0)',
    )
    condition_total_solved = models.PositiveIntegerField(
        default=0,
        help_text="Общее кол-во решённых задач (для type='total')",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Бейдж'
        verbose_name_plural = 'Бейджи'

    def __str__(self):
        return f'{self.icon} {self.title}'

    def clean(self):
        if self.type == 'subject' and not self.condition_subject:
            raise ValidationError("Для типа 'По предмету' нужно указать предмет.")

        if self.type == 'total' and self.condition_total_solved == 0:
            raise ValidationError("Для типа 'Общие' нужно указать condition_total_solved > 0.")

        if self.type == 'pvp' and self.condition_min_solved == 0:
            raise ValidationError("Для типа 'PvP' нужно указать condition_min_solved > 0.")

    def check_condition(self, user):
        if self.type == 'subject':
            if not self.condition_subject:
                return False

            attempts = TaskAttempt.objects.filter(user=user, subject=self.condition_subject)
            solved = attempts.count()
            correct = attempts.filter(is_correct=True).count()
            ratio = correct / solved if solved else 0
            return solved >= self.condition_min_solved and ratio >= float(self.condition_min_correct_ratio)

        if self.type == 'total':
            return TaskAttempt.objects.filter(user=user).count() >= self.condition_total_solved

        if self.type == 'pvp':
            wins = Match.objects.filter(
                status='finished',
            ).filter(
                (Q(player1=user) & Q(player1_correct=True) & Q(player2_correct=False))
                | (Q(player2=user) & Q(player2_correct=True) & Q(player1_correct=False))
            ).count()
            return wins >= self.condition_min_solved

        # `streak` not implemented in current domain model
        return False


class UserBadge(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено (ожидает выдачи)'),
        ('earned', 'Получен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    class Meta:
        unique_together = ('user', 'badge')
        verbose_name = 'Бейдж пользователя'
        verbose_name_plural = 'Бейджи пользователей'

    def __str__(self):
        return f'{self.user.username} — {self.badge.title} ({self.status})'
