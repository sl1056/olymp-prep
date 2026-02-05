from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from tasks.models import Task
from .models import Match
from .serializers import MatchSerializer
import random

class CreateMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subject = request.data.get('subject')
        difficulty = request.data.get('difficulty')

        tasks = Task.objects.all()
        if subject:
            tasks = tasks.filter(subject=subject)
        if difficulty:
            tasks = tasks.filter(difficulty=difficulty)

        if not tasks.exists():
            return Response(
                {"error": "Нет задач по заданным критериям"},
                status=status.HTTP_400_BAD_REQUEST
            )

        task = random.choice(tasks)

        match = Match.objects.create(
            player1=request.user,
            task=task
        )

        return Response(MatchSerializer(match).data, status=status.HTTP_201_CREATED)


class JoinMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, match_id):
        match = get_object_or_404(Match, id=match_id, status='waiting')
        if match.player1 == request.user:
            return Response(
                {"error": "Вы уже создали этот матч"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if match.player2 is not None:
            return Response(
                {"error": "Матч уже заполнен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        match.player2 = request.user
        match.status = 'active'
        match.started_at = timezone.now()
        match.save()

        return Response(MatchSerializer(match).data, status=status.HTTP_200_OK)


class MatchStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        if match.player1 != request.user and match.player2 != request.user:
            return Response(
                {"error": "Матч не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(MatchSerializer(match).data)