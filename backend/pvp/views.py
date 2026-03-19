<<<<<<< Updated upstream
import uuid
from django.shortcuts import render
=======
# pvp/views.py
import random
from datetime import timedelta
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db import transaction
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import QuizRoom
from tasks.models import Task


def _parse_bool(value, default=False):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {'1', 'true', 'yes', 'on'}
    return default


def _build_selected_tasks(tasks, questions_count, random_order):
    if not tasks:
        return []

    if random_order:
        selected = []
        while len(selected) < questions_count:
            chunk = list(tasks)
            random.shuffle(chunk)
            selected.extend(chunk)
        return selected[:questions_count]

    ordered_tasks = sorted(tasks, key=lambda item: item.id)
    selected = []
    while len(selected) < questions_count:
        selected.extend(ordered_tasks)
    return selected[:questions_count]


def _time_left_seconds(match):
    if (
        not match.timer_enabled
        or not match.time_limit_seconds
        or not match.current_question_started_at
        or match.status != 'active'
    ):
        return None

    deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
    return max(0, int((deadline - timezone.now()).total_seconds()))


def _sync_match_timeout(match_id):
    with transaction.atomic():
        match = Match.objects.select_for_update().get(id=match_id)

        if (
            match.status != 'active'
            or not match.timer_enabled
            or not match.time_limit_seconds
            or not match.current_question_started_at
        ):
            return

        deadline = match.current_question_started_at + timedelta(seconds=match.time_limit_seconds)
        if timezone.now() < deadline:
            return

        update_fields = []
        if not match.player1_submitted_at:
            match.player1_submitted_at = deadline
            match.player1_answer = ''
            match.player1_correct = False
            update_fields.extend(['player1_submitted_at', 'player1_answer', 'player1_correct'])

        if not match.player2_submitted_at:
            match.player2_submitted_at = deadline
            match.player2_answer = ''
            match.player2_correct = False
            update_fields.extend(['player2_submitted_at', 'player2_answer', 'player2_correct'])

        if update_fields:
            match.save(update_fields=update_fields)

        if match.player1_submitted_at and match.player2_submitted_at:
            # Import locally to avoid circular imports at module load time.
            from .consumers import MatchConsumer
            MatchConsumer()._finalize_match_logic(match.id)


class CreateMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
<<<<<<< Updated upstream
        room = find_or_create_room(request.user)
        return Response({
            "match_id": room.id,
            "room_id": room.room_id,
            "waiting_for_opponent": room.player2 is None
=======
        subject = request.data.get('subject')
        topic = request.data.get('topic')
        difficulty = request.data.get('difficulty')
        raw_questions_count = request.data.get('questions_count', 1)
        timer_enabled = _parse_bool(request.data.get('timer_enabled'), default=True)
        hints_enabled = _parse_bool(request.data.get('hints_enabled'), default=False)
        random_order = _parse_bool(request.data.get('random_order'), default=True)
        is_private = _parse_bool(request.data.get('is_private'), default=False)

        try:
            requested_questions_count = int(raw_questions_count)
        except (TypeError, ValueError):
            return Response({"error": "Количество вопросов должно быть целым числом"}, status=400)

        if requested_questions_count < 1 or requested_questions_count > 20:
            return Response({"error": "Количество вопросов должно быть от 1 до 20"}, status=400)

        raw_time_limit_seconds = request.data.get('time_limit_seconds', 600)
        if timer_enabled:
            try:
                time_limit_seconds = int(raw_time_limit_seconds)
            except (TypeError, ValueError):
                return Response({"error": "Лимит времени должен быть целым числом"}, status=400)
            if time_limit_seconds < 30 or time_limit_seconds > 3600:
                return Response({"error": "Лимит времени должен быть от 30 до 3600 секунд"}, status=400)
        else:
            time_limit_seconds = None

        tasks = Task.objects.all()
        if subject:
            tasks = tasks.filter(subject=subject)
        if topic:
            tasks = tasks.filter(topic=topic)
        if difficulty:
            tasks = tasks.filter(difficulty=difficulty)

        if not tasks.exists():
            return Response({"error": "Нет задач по заданным критериям"}, status=400)

        available_tasks = list(tasks)
        selected_tasks = _build_selected_tasks(
            tasks=available_tasks,
            questions_count=requested_questions_count,
            random_order=random_order,
        )
        first_task = selected_tasks[0]
        private_token = get_random_string(24) if is_private else ''

        match = Match.objects.create(
            player1=request.user,
            task=first_task,
            status='waiting',
            questions_count=requested_questions_count,
            current_question_index=1,
            question_task_ids=[task.id for task in selected_tasks],
            timer_enabled=timer_enabled,
            hints_enabled=hints_enabled,
            random_order=random_order,
            is_private=is_private,
            private_token=private_token,
            time_limit_seconds=time_limit_seconds,
            current_question_started_at=None,
        )

        share_link = f"/PvP?join={match.id}"
        if match.is_private:
            share_link = f"{share_link}&token={match.private_token}"

        return Response({
            "match_id": match.id,
            "match_code": str(match.id),
            "join_code": (
                f"{match.id}:{match.private_token}"
                if match.is_private else str(match.id)
            ),
            "status": match.status,
            "subject": match.task.subject,
            "difficulty": match.task.difficulty,
            "task_text": match.task.text,
            "questions_count": match.questions_count,
            "current_question_index": match.current_question_index,
            "player1_score": match.player1_score,
            "player2_score": match.player2_score,
            "timer_enabled": match.timer_enabled,
            "hints_enabled": match.hints_enabled,
            "random_order": match.random_order,
            "is_private": match.is_private,
            "private_token": match.private_token if match.is_private else None,
            "time_limit_seconds": match.time_limit_seconds,
            "share_link": share_link,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        }, status=status.HTTP_201_CREATED)


class JoinMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, match_id):
<<<<<<< Updated upstream
        room = get_object_or_404(QuizRoom, id=match_id)
        
        if room.player1 == request.user:
            return Response({"error": "You are already in this match"}, status=status.HTTP_400_BAD_REQUEST)
        
        if room.player2 is not None:
            return Response({"error": "Match is already full"}, status=status.HTTP_400_BAD_REQUEST)
        
        room.player2 = request.user
        room.save()
        
        return Response({
            "match_id": room.id,
            "room_id": room.room_id,
            "joined": True
        })
=======
        try:

            match = Match.objects.get(id=match_id, status='waiting')
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

        if match.player2:
            return Response(
                {"error": "Матч уже заполнен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        provided_token = request.data.get('token') or request.query_params.get('token')
        if match.is_private and provided_token != match.private_token:
            return Response(
                {"error": "Неверный токен приглашения для закрытого матча"},
                status=status.HTTP_403_FORBIDDEN
            )

        match.player2 = request.user
        match.status = 'active'
        match.started_at = timezone.now()
        match.current_question_started_at = timezone.now()
        match.save(update_fields=['player2', 'status', 'started_at', 'current_question_started_at'])

        return Response({
            "match_id": match.id,
            "match_code": str(match.id),
            "join_code": (
                f"{match.id}:{match.private_token}"
                if match.is_private else str(match.id)
            ),
            "status": match.status,
            "subject": match.task.subject,
            "difficulty": match.task.difficulty,
            "task_text": match.task.text,
            "questions_count": match.questions_count,
            "current_question_index": match.current_question_index,
            "player1_score": match.player1_score,
            "player2_score": match.player2_score,
            "timer_enabled": match.timer_enabled,
            "hints_enabled": match.hints_enabled,
            "random_order": match.random_order,
            "is_private": match.is_private,
            "time_limit_seconds": match.time_limit_seconds,
            "player1": match.player1.username,
            "player2": match.player2.username
        }, status=status.HTTP_200_OK)
>>>>>>> Stashed changes


class MatchStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
<<<<<<< Updated upstream
        room = get_object_or_404(QuizRoom, id=match_id)
        
        return Response({
            "match_id": room.id,
            "room_id": room.room_id,
            "player1": room.player1.username,
            "player2": room.player2.username if room.player2 else None,
            "score_p1": room.score_p1,
            "score_p2": room.score_p2,
            "current_task_index": room.current_task_index,
            "is_active": room.is_active,
            "ready": room.player2 is not None
        })


def find_or_create_room(user):
    
    room = QuizRoom.objects.filter(player2__isnull=True, is_active=True).exclude(player1=user).first()
    
    if room:
        room.player2 = user
        room.save()
    else:
        room = QuizRoom.objects.create(
            room_id=str(uuid.uuid4())[:8],
            player1=user
        )
        random_tasks = Task.objects.order_by('?')[:5]
        room.tasks.set(random_tasks)
    
    return room
=======
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

        _sync_match_timeout(match.id)
        match.refresh_from_db()

        response_data = {
            "match_id": match.id,
            "match_code": str(match.id),
            "status": match.status,
            "subject": match.task.subject,
            "difficulty": match.task.difficulty,
            "player1": match.player1.username,
            "player2": match.player2.username if match.player2 else None,
            "player1_answered": bool(match.player1_submitted_at),
            "player2_answered": bool(match.player2_submitted_at),
            "you_answered": (
                bool(match.player1_submitted_at)
                if match.player1_id == request.user.id
                else bool(match.player2_submitted_at)
            ),
            "questions_count": match.questions_count,
            "current_question_index": match.current_question_index,
            "player1_score": match.player1_score,
            "player2_score": match.player2_score,
            "timer_enabled": match.timer_enabled,
            "hints_enabled": match.hints_enabled,
            "random_order": match.random_order,
            "is_private": match.is_private,
            "time_limit_seconds": match.time_limit_seconds,
            "time_left_seconds": _time_left_seconds(match),
            "task_hints": (match.task.hints or []) if match.hints_enabled else [],
            "task_text": match.task.text,
            "started_at": match.started_at,
            "finished_at": match.finished_at
        }

        if match.status == 'finished' and match.player2:
            if match.player1_score > match.player2_score:
                winner = 'player1'
            elif match.player2_score > match.player1_score:
                winner = 'player2'
            else:
                winner = 'draw'

            response_data["result"] = {
                "match_id": match.id,
                "winner": winner,
                "player1_username": match.player1.username,
                "player2_username": match.player2.username,
                "player1_new_rating": match.player1.profile.rating,
                "player2_new_rating": match.player2.profile.rating,
                "player1_score": match.player1_score,
                "player2_score": match.player2_score,
                "total_questions": match.questions_count,
                "player1_correct": match.player1_correct,
                "player2_correct": match.player2_correct,
                "correct_answer": match.task.correct_answer,
            }

        return Response(response_data)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
