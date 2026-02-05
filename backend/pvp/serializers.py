from rest_framework import serializers
from .models import Match
from tasks.serializers import TaskSerializer

class MatchSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    player1_username = serializers.CharField(source='player1.username', read_only=True)
    player2_username = serializers.CharField(source='player2.username', read_only=True)

    class Meta:
        model = Match
        fields = (
            'id', 'status', 'created_at', 'started_at', 'finished_at',
            'player1_username', 'player2_username',
            'task',
            'player1_submitted_at', 'player2_submitted_at'
        )