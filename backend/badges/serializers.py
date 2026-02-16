from rest_framework import serializers
from .models import Badge, UserBadge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

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