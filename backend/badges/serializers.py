from rest_framework import serializers

from analytics.models import TaskAttempt
from .models import Badge, UserBadge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class BadgeProgressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    icon = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    condition_subject = serializers.CharField(read_only=True, allow_null=True)
    condition_min_solved = serializers.IntegerField(read_only=True)
    condition_min_correct_ratio = serializers.DecimalField(
        max_digits=4, decimal_places=2, read_only=True
    )
    condition_total_solved = serializers.IntegerField(read_only=True)

    status = serializers.CharField(read_only=True)
    progress = serializers.DictField(read_only=True)
    earned_at = serializers.DateTimeField(read_only=True, allow_null=True)

    def to_representation(self, instance):
        user = self.context['request'].user
        badge = instance

        progress_data = {}
        status_val = 'in_progress'

        if badge.type == 'subject':
            if badge.condition_subject:
                attempts = TaskAttempt.objects.filter(
                    user=user, subject=badge.condition_subject
                )
                solved = attempts.count()
                correct = attempts.filter(is_correct=True).count()
                ratio = correct / solved if solved > 0 else 0

                progress_data = {
                    'solved': solved,
                    'needed': badge.condition_min_solved,
                    'ratio': round(ratio, 2),
                    'ratio_needed': float(badge.condition_min_correct_ratio)
                }

                if solved >= badge.condition_min_solved and ratio >= badge.condition_min_correct_ratio:
                    status_val = 'earned'
                elif solved >= badge.condition_min_solved:
                    status_val = 'completed'


        elif badge.type == 'total':
            total_solved = TaskAttempt.objects.filter(user=user).count()
            progress_data = {
                'solved': total_solved,
                'needed': badge.condition_total_solved,
                'ratio': None,
                'ratio_needed': None
            }
            if total_solved >= badge.condition_total_solved:
                status_val = 'earned'

        earned_at = None
        try:
            ub = badge.user_badges.get(user=user)
            earned_at = ub.earned_at if ub.status == 'earned' else None
        except badge.user_badges.model.DoesNotExist:
            pass

        return {
            'id': badge.id,
            'title': badge.title,
            'icon': badge.icon,
            'description': badge.description,
            'type': badge.type,
            'condition_subject': badge.condition_subject,
            'condition_min_solved': badge.condition_min_solved,
            'condition_min_correct_ratio': badge.condition_min_correct_ratio,
            'condition_total_solved': badge.condition_total_solved,
            'status': status_val,
            'progress': progress_data,
            'earned_at': earned_at,
        }
class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'status', 'earned_at', 'progress']

    def get_progress(self, obj):
        if obj.badge.type == 'subject':
            user = obj.user
            subject = obj.badge.condition_subject
            attempts = user.attempts.filter(subject=subject)
            solved = attempts.count()
            correct = attempts.filter(is_correct=True).count()
            ratio = correct / solved if solved > 0 else 0
            needed = obj.badge.condition_min_solved
            return {
                'solved': solved,
                'needed': needed,
                'ratio': round(ratio, 2),
                'ratio_needed': float(obj.badge.condition_min_correct_ratio)
            }
        return None