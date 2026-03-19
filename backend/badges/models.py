# badges/models.py
from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task
from django.utils import timezone
from django.core.exceptions import ValidationError


class Badge(models.Model):
    TYPE_CHOICES = [
        ('subject', 'По предмету'),
        ('total', 'Общие'),
        ('streak', 'Серии'),
        ('pvp', 'PvP'),
    ]

    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    icon = models.CharField(
        max_length=50,
        default="⭐",
        help_text="Эмодзи или короткий код иконки (напр. 🧮, 🧪, 💻)"
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='subject')
    condition_subject = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Предмет (например: 'math', 'phys') — только для type='subject'"
    )
    condition_min_solved = models.PositiveIntegerField(
        default=0,
        help_text="Мин. количество решённых задач"
    )
    condition_min_correct_ratio = models.DecimalField(
        max_digits=4, decimal_places=2,
        default=0.0,
        help_text="Мин. % правильных ответов (0.0–1.0)"
    )
    condition_total_solved = models.PositiveIntegerField(
        default=0,
        help_text="Общее кол-во решённых задач (для type='total')"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бейдж"
        verbose_name_plural = "Бейджи"

    def __str__(self):
        return f"{self.icon} {self.title}"

    def clean(self):
        if self.type == 'subject':
            if not self.condition_subject:
                raise ValidationError("Для типа 'По предмету' нужно указать предмет.")
        elif self.type == 'total':
            if self.condition_total_solved == 0:
                raise ValidationError("Для типа 'Общие' нужно указать min_total_solved > 0.")

    def check_condition(self, user):

        if self.type == 'subject':
            if not self.condition_subject:
                return False

            attempts = user.attempts.filter(subject=self.condition_subject)
            solved = attempts.count()
            correct = attempts.filter(is_correct=True).count()

            ratio = correct / solved if solved > 0 else 0
            return (
                    solved >= self.condition_min_solved and
                    ratio >= self.condition_min_correct_ratio
            )

        elif self.type == 'total':
            total_solved = user.attempts.count()
            return total_solved >= self.condition_total_solved

        elif self.type == 'streak':
            return False

        elif self.type == 'pvp':
            from pvp.models import Match
            wins = Match.objects.filter(
                player1=user, status='finished', player1_correct=True
            ).count() + Match.objects.filter(
                player2=user, status='finished', player2_correct=True
            ).count()
            return wins >= self.condition_min_solved

        return False


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[
            ('in_progress', 'В процессе'),
            ('completed', 'Выполнено (ожидает выдачи)'),
            ('earned', 'Получен'),
        ],
        default='in_progress'
    )

    class Meta:
        unique_together = ('user', 'badge')
        verbose_name = "Бейдж пользователя"
        verbose_name_plural = "Бейджи пользователей"

    def __str__(self):
        return f"{self.user.username} — {self.badge.title} ({self.status})"