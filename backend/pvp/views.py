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
            task=task,
            status='waiting'
        )

        match_code = str(match.id)

        return Response({
            "match_id": match.id,
            "match_code": match_code,
            "status": match.status,
            "task_text": match.task.text,
            "share_link": f"/join/{match_code}"
        }, status=status.HTTP_201_CREATED)


class JoinMatchView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, match_code):
        try:
            match = Match.objects.get(id=match_code)
        except Match.DoesNotExist:
            return Response({"error": "Матч не найден"}, status=status.HTTP_404_NOT_FOUND)

        if match.status != 'waiting':
            if match.status == 'active':
                return Response({"error": "Матч уже начался"}, status=status.HTTP_400_BAD_REQUEST)
            elif match.status == 'finished':
                return Response({"error": "Матч уже завершен"}, status=status.HTTP_400_BAD_REQUEST)
            elif match.status == 'cancelled':
                return Response({"error": "Матч отменен"}, status=status.HTTP_400_BAD_REQUEST)

        if match.player1 == request.user:
            return Response({"error": "Вы уже создали этот матч"}, status=status.HTTP_400_BAD_REQUEST)

        if match.player2:
            return Response({"error": "Матч уже заполнен"}, status=status.HTTP_400_BAD_REQUEST)

        match.player2 = request.user
        match.status = 'active'
        match.started_at = timezone.now()
        match.save()
        return Response({
            "match_id": match.id,
            "match_code": match_code,
            "status": match.status,
            "task_text": match.task.text,
            "player1": match.player1.username,
            "player2": match.player2.username
        }, status=status.HTTP_200_OK)


class MatchStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_code):
        match = get_object_or_404(Match, id=match_code)

        is_participant = (
                match.player1 == request.user or
                (match.player2 and match.player2 == request.user)
        )

        if not is_participant:
            return Response({"error": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)

        return Response({
            "match_id": match.id,
            "match_code": str(match.id),
            "status": match.status,
            "player1": match.player1.username,
            "player2": match.player2.username if match.player2 else None,
            "player1_answered": bool(match.player1_submitted_at),
            "player2_answered": bool(match.player2_submitted_at),
            "task_text": match.task.text,
            "started_at": match.started_at,
            "finished_at": match.finished_at
        })