# badges/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Badge, UserBadge
from analytics.models import TaskAttempt
from pvp.models import Match
from users.models import Profile

@receiver(post_save, sender=TaskAttempt)
def update_badge_progress_on_attempt(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    subject = instance.subject
    for badge in Badge.objects.filter(type='subject', condition_subject=subject):
        try:
            ub = UserBadge.objects.get(user=user, badge=badge)
        except UserBadge.DoesNotExist:
            ub = UserBadge.objects.create(user=user, badge=badge, status='in_progress')

        if badge.check_condition(user):
            if ub.status == 'in_progress':
                ub.status = 'completed'
                ub.save()
        else:
            ub.status = 'in_progress'
            ub.save()

@receiver(post_save, sender=Match)
def update_pvp_badges(sender, instance, created, **kwargs):
    if not created or instance.status != 'finished':
        return

    user1, user2 = instance.player1, instance.player2
    for user in [user1, user2]:
        for badge in Badge.objects.filter(type='pvp'):
            try:
                ub = UserBadge.objects.get(user=user, badge=badge)
            except UserBadge.DoesNotExist:
                ub = UserBadge.objects.create(user=user, badge=badge, status='in_progress')

            if badge.check_condition(user):
                if ub.status == 'in_progress':
                    ub.status = 'completed'
                    ub.save()