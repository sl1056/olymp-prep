from rest_framework import serializers
from .models import TaskAttempt
from tasks.models import Task


class AttemptSerializer(serializers.ModelSerializer):
    task_text = serializers.CharField(source='task.text', read_only=True)
    task_subject = serializers.CharField(source='task.get_subject_display', read_only=True)
    task_difficulty = serializers.CharField(source='task.get_difficulty_display', read_only=True)

    class Meta:
        model = TaskAttempt
        fields = (
            'id', 'task_text', 'task_subject', 'task_difficulty',
            'is_correct', 'submitted_at'
        )


class OverallStatsSerializer(serializers.Serializer):
    username = serializers.CharField()
    total_attempts = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    accuracy = serializers.FloatField()
    accuracy_percent = serializers.FloatField()
    def get_accuracy_percent(self, obj):
        return round(obj['accuracy'] * 100, 1) if obj['accuracy'] else 0.0


class SubjectStatsSerializer(serializers.Serializer):
    subject_code = serializers.CharField()
    subject_name = serializers.CharField()
    total_attempts = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    accuracy = serializers.FloatField()


class DifficultyStatsSerializer(serializers.Serializer):
    difficulty = serializers.CharField()
    difficulty_name = serializers.CharField()
    total_attempts = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    accuracy = serializers.FloatField()