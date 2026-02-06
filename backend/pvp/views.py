import random
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Match
from tasks.models import Task

class CreateMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subject = request.data.get('subject')
        topic = request.data.get('topic')
        difficulty = request.data.get('difficulty')

        tasks = Task.objects.all()
        if subject:
            tasks = tasks.filter(subject=subject)
        if topic:
            tasks = tasks.filter(topic=topic)
        if difficulty:
            tasks = tasks.filter(difficulty=difficulty)

        if not tasks.exists():
            return Response({"error": "Нет задач по заданным критериям"}, status=400)

        task = random.choice(tasks)

        match = Match.objects.create(
            player1=request.user,
            task=task
        )

        return Response({
            "match_id": match.id,
            "status": match.status,
            "task_text": match.task.text,
            "share_link": f"/pvp?match_id={match.id}"
        }, status=status.HTTP_201_CREATED)


class JoinMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, match_id):
        match = get_object_or_404(Match, id=match_id, status='waiting')
        if match.player1 == request.user:
            return Response({"error": "Вы уже создали этот матч"}, status=400)
        if match.player2:
            return Response({"error": "Матч уже заполнен"}, status=400)

        match.player2 = request.user
        match.status = 'active'
        match.started_at = timezone.now()
        match.save()

        return Response({
            "match_id": match.id,
            "status": match.status,
            "task_text": match.task.text
        })


class MatchStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        if match.player1 != request.user and match.player2 != request.user:
            return Response({"error": "Доступ запрещён"}, status=403)

        return Response({
            "match_id": match.id,
            "status": match.status,
            "player1": match.player1.username,
            "player2": match.player2.username if match.player2 else None,
            "player1_answered": bool(match.player1_submitted_at),
            "player2_answered": bool(match.player2_submitted_at),
            "task_text": match.task.text,
            "started_at": match.started_at,
            "finished_at": match.finished_at
        })