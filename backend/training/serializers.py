from rest_framework import serializers

from tasks.models import Task


class StartTrainingRequestSerializer(serializers.Serializer):
    subject = serializers.ChoiceField(choices=Task.SUBJECTS)
    tasks_count = serializers.IntegerField(min_value=1)


class SubmitTrainingAnswerRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(min_value=1)
    task_id = serializers.IntegerField(min_value=1)
    answer = serializers.CharField(allow_blank=False, trim_whitespace=True, max_length=255)
