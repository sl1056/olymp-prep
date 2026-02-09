from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import TaskAttempt
from .serializers import (
    AttemptSerializer,
    OverallStatsSerializer,
    SubjectStatsSerializer,
    DifficultyStatsSerializer
)
from tasks.models import Task

class OverallStatsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_attempts = TaskAttempt.objects.filter(user=user).count()
        correct_answers = TaskAttempt.objects.filter(user=user, is_correct=True).count()
        accuracy = (correct_answers / total_attempts) if total_attempts > 0 else 0

        data = {
            'username': user.username,
            'total_attempts': total_attempts,
            'correct_answers': correct_answers,
            'accuracy': accuracy,
            'accuracy_percent': round(accuracy * 100, 1) if total_attempts > 0 else 0.0
        }

        serializer = OverallStatsSerializer(data)
        return Response(serializer.data)


class SubjectStatsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        subjects = TaskAttempt.objects.filter(user=user) \
            .values('subject') \
            .annotate(
            total_attempts=Count('id'),
            correct_answers=Count('id', filter=Q(is_correct=True))
        ) \
            .order_by('-total_attempts')

        result = []
        for item in subjects:
            subject_code = item['subject']
            subject_name = dict(Task.SUBJECTS).get(subject_code, subject_code)

            total = item['total_attempts']
            correct = item['correct_answers']
            accuracy = (correct / total) if total > 0 else 0

            result.append({
                'subject_code': subject_code,
                'subject_name': subject_name,
                'total_attempts': total,
                'correct_answers': correct,
                'accuracy': accuracy
            })

        serializer = SubjectStatsSerializer(result, many=True)
        return Response(serializer.data)


class DifficultyStatsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        difficulties = TaskAttempt.objects.filter(user=user) \
            .values('difficulty') \
            .annotate(
            total_attempts=Count('id'),
            correct_answers=Count('id', filter=Q(is_correct=True))
        ) \
            .order_by('difficulty')

        result = []
        difficulty_names = dict(Task.DIFFICULTY_CHOICES)

        for item in difficulties:
            difficulty = item['difficulty']

            result.append({
                'difficulty': difficulty,
                'difficulty_name': difficulty_names.get(difficulty, difficulty),
                'total_attempts': item['total_attempts'],
                'correct_answers': item['correct_answers'],
                'accuracy': (item['correct_answers'] / item['total_attempts'])
                if item['total_attempts'] > 0 else 0
            })

        serializer = DifficultyStatsSerializer(result, many=True)
        return Response(serializer.data)


class RecentAttemptsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        attempts = TaskAttempt.objects.filter(user=request.user)[:20]
        serializer = AttemptSerializer(attempts, many=True)
        return Response(serializer.data)

class SubjectsChartDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        subjects = TaskAttempt.objects.filter(user=user) \
            .values('subject') \
            .annotate(
                total=Count('id'),
                correct=Count('id', filter=Q(is_correct=True))
            )

        labels = []
        data = []
        for item in subjects:
            subject_code = item['subject']
            subject_name = dict(Task.SUBJECTS).get(subject_code, subject_code)
            total = item['total']
            correct = item['correct']
            accuracy = round((correct / total) * 100, 1) if total > 0 else 0

            labels.append(subject_name)
            data.append(accuracy)

        return Response({
            "labels": labels,
            "data": data
        })

class AccuracyChartDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total = TaskAttempt.objects.filter(user=user).count()
        correct = TaskAttempt.objects.filter(user=user, is_correct=True).count()
        incorrect = total - correct

        return Response([
            {"name": "Правильно", "value": correct, "color": "#06D6A0"},
            {"name": "Неправильно", "value": incorrect, "color": "#EF476F"}
        ])