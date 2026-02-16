from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.models import TaskAttempt
from pvp.models import Match

from .models import Badge, UserBadge


def sync_user_badges(user):
    for badge in Badge.objects.all():
        status = 'earned' if badge.check_condition(user) else 'in_progress'
        user_badge, _ = UserBadge.objects.get_or_create(user=user, badge=badge)

        if user_badge.status != status:
            user_badge.status = status
            user_badge.save(update_fields=['status'])


@receiver(post_save, sender=TaskAttempt)
def update_badges_on_attempt(sender, instance, created, **kwargs):
    if created:
        sync_user_badges(instance.user)


@receiver(post_save, sender=Match)
def update_badges_on_match(sender, instance, **kwargs):
    if instance.status != 'finished':
        return

    sync_user_badges(instance.player1)
    if instance.player2_id:
        sync_user_badges(instance.player2)
