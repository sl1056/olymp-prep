# pvp/views.py
import random
from django.utils import timezone
from django.db import transaction
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
        raw_question_count = request.data.get('question_count', request.data.get('questions_count', 1))

        try:
            question_count = int(raw_question_count)
        except (TypeError, ValueError):
            return Response({"error": "Некорректное количество вопросов"}, status=400)

        if question_count < 1 or question_count > 20:
            return Response({"error": "Количество вопросов должно быть от 1 до 20"}, status=400)

        tasks = Task.objects.all()
        if subject:
            tasks = tasks.filter(subject=subject)
        if topic:
            tasks = tasks.filter(topic=topic)
        if difficulty:
            tasks = tasks.filter(difficulty=difficulty)

        task_ids = list(tasks.values_list('id', flat=True))
        if not task_ids:
            return Response({"error": "Нет задач по заданным критериям"}, status=400)

        if len(task_ids) < question_count:
            return Response(
                {"error": f"Недостаточно задач: доступно {len(task_ids)}, запрошено {question_count}"},
                status=400
            )

        selected_task_ids = random.sample(task_ids, question_count)
        first_task = Task.objects.get(id=selected_task_ids[0])

        match = Match.objects.create(
            player1=request.user,
            task=first_task,
            status='waiting',
            player1_score=0,
            player2_score=0,
            current_question_index=1,
            question_task_ids=selected_task_ids,
            questions_count=question_count,
        )

        return Response({
            "match_id": match.id,
            "match_code": str(match.id),
            "status": match.status,
            "task_text": match.task.text,
            "current_question_index": match.current_question_index,
            "questions_count": match.questions_count,
            "share_link": f"/join/{match.id}"
        }, status=status.HTTP_201_CREATED)


class JoinMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, match_id):
        with transaction.atomic():
            try:
                # Lock row to prevent two players from joining at the same time.
                match = Match.objects.select_for_update().get(id=match_id)
            except Match.DoesNotExist:
                return Response(
                    {"error": "Матч не найден или уже начался"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if match.player1 == request.user:
                return Response(
                    {"error": "Вы уже создали этот матч"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if match.status != 'waiting':
                # Allow idempotent re-join for the second player in active matches.
                if match.status == 'active' and match.player2 == request.user:
                    return Response({
                        "match_id": match.id,
                        "match_code": str(match.id),
                        "status": match.status,
                        "task_text": match.task.text,
                        "current_question_index": match.current_question_index,
                        "questions_count": match.questions_count,
                        "player1": match.player1.username,
                        "player2": match.player2.username
                    }, status=status.HTTP_200_OK)

                return Response(
                    {"error": "Матч не найден или уже начался"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if match.player2 and match.player2 != request.user:
                return Response(
                    {"error": "Матч уже заполнен"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            match.player2 = request.user
            match.status = 'active'
            match.started_at = timezone.now()
            match.save(update_fields=['player2', 'status', 'started_at'])

        return Response({
            "match_id": match.id,
            "match_code": str(match.id),
            "status": match.status,
            "task_text": match.task.text,
            "current_question_index": match.current_question_index,
            "questions_count": match.questions_count,
            "player1": match.player1.username,
            "player2": match.player2.username
        }, status=status.HTTP_200_OK)


class MatchStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)

        is_participant = (
            match.player1 == request.user or
            (match.player2 and match.player2 == request.user)
        )

        if not is_participant:
            return Response(
                {"error": "Доступ запрещён"},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response({
            "match_id": match.id,
            "match_code": str(match.id),
            "status": match.status,
            "player1": match.player1.username,
            "player2": match.player2.username if match.player2 else None,
            "player1_answered": bool(match.player1_submitted_at),
            "player2_answered": bool(match.player2_submitted_at),
            "task_text": match.task.text,
            "current_question_index": match.current_question_index,
            "questions_count": match.questions_count,
            "player1_score": match.player1_score,
            "player2_score": match.player2_score,
            "started_at": match.started_at,
            "finished_at": match.finished_at
        })
