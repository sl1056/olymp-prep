from django.db.models import Q
from rest_framework import serializers

from analytics.models import TaskAttempt
from pvp.models import Match
from .models import Badge


class BadgeProgressSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    earned_at = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    bgColor = serializers.SerializerMethodField()
    difficultyLevel = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = (
            'id',
            'title',
            'description',
            'icon',
            'type',
            'condition_subject',
            'condition_min_solved',
            'condition_min_correct_ratio',
            'condition_total_solved',
            'status',
            'progress',
            'earned_at',
            'completed',
            'bgColor',
            'difficultyLevel',
        )

    def _user(self):
        return self.context['request'].user

    def _subject_progress(self, badge, user):
        attempts = TaskAttempt.objects.filter(user=user, subject=badge.condition_subject)
        solved = attempts.count()
        correct = attempts.filter(is_correct=True).count()
        ratio = correct / solved if solved else 0
        needed = badge.condition_min_solved
        return {
            'solved': solved,
            'needed': max(needed, 1),
            'ratio': round(ratio, 2),
            'ratio_needed': float(badge.condition_min_correct_ratio),
        }

    def _total_progress(self, badge, user):
        solved = TaskAttempt.objects.filter(user=user).count()
        needed = badge.condition_total_solved
        return {
            'solved': solved,
            'needed': max(needed, 1),
            'ratio': None,
            'ratio_needed': None,
        }

    def _pvp_progress(self, badge, user):
        wins = Match.objects.filter(
            status='finished',
        ).filter(
            (Q(player1=user) & Q(player1_correct=True) & Q(player2_correct=False))
            | (Q(player2=user) & Q(player2_correct=True) & Q(player1_correct=False))
        ).count()
        return {
            'solved': wins,
            'needed': max(badge.condition_min_solved, 1),
            'ratio': None,
            'ratio_needed': None,
        }

    def get_progress(self, badge):
        user = self._user()
        if badge.type == 'subject' and badge.condition_subject:
            return self._subject_progress(badge, user)
        if badge.type == 'total':
            return self._total_progress(badge, user)
        if badge.type == 'pvp':
            return self._pvp_progress(badge, user)
        return {'solved': 0, 'needed': 1, 'ratio': None, 'ratio_needed': None}

    def get_status(self, badge):
        user = self._user()
        if badge.check_condition(user):
            return 'earned'
        return 'in_progress'

    def get_earned_at(self, badge):
        user = self._user()
        ub = badge.user_badges.filter(user=user, status='earned').first()
        return ub.earned_at if ub else None

    def get_completed(self, badge):
        return self.get_status(badge) == 'earned'

    def get_bgColor(self, badge):
        return {
            'subject': '#4A7B9D',
            'total': '#06D6A0',
            'pvp': '#EF476F',
            'streak': '#FFD166',
        }.get(badge.type, '#4A7B9D')

    def get_difficultyLevel(self, badge):
        threshold = max(
            badge.condition_min_solved,
            badge.condition_total_solved,
            1,
        )
        if threshold >= 50:
            return 'Эксперт'
        if threshold >= 20:
            return 'Продвинутый'
        return 'Новичок'
