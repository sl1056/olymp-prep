from django.contrib.auth.models import User
from rest_framework import serializers

from pvp.models import Match
from tasks.models import Task


class AdminUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
            'role',
        )

    def get_role(self, obj):
        if obj.is_superuser:
            return 'superadmin'
        if obj.is_staff:
            return 'admin'
        return 'user'


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['user', 'admin', 'superadmin'], required=False)

    class Meta:
        model = User
        fields = ('is_active', 'role')

    def update(self, instance, validated_data):
        role = validated_data.pop('role', None)
        if role == 'user':
            instance.is_staff = False
            instance.is_superuser = False
        elif role == 'admin':
            instance.is_staff = True
            instance.is_superuser = False
        elif role == 'superadmin':
            instance.is_staff = True
            instance.is_superuser = True

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AdminTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'subject', 'topic', 'difficulty', 'text', 'hints', 'correct_answer')


class AdminMatchResultSerializer(serializers.ModelSerializer):
    task_subject = serializers.CharField(source='task.subject', read_only=True)
    task_topic = serializers.CharField(source='task.topic', read_only=True)
    winner = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = (
            'id',
            'status',
            'player1',
            'player2',
            'player1_correct',
            'player2_correct',
            'created_at',
            'finished_at',
            'task_subject',
            'task_topic',
            'winner',
        )

    def get_winner(self, obj):
        if not obj.player2:
            return None
        if obj.player1_correct and not obj.player2_correct:
            return obj.player1.username
        if obj.player2_correct and not obj.player1_correct:
            return obj.player2.username
        return 'draw'


class ExternalApiCheckSerializer(serializers.Serializer):
    url = serializers.URLField()
