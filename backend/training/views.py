from django.shortcuts import render
import random

# Create your views here.
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import TaskAttempt
from tasks.models import Task

from .models import TrainingAnswer, TrainingSession


class StartTrainingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subject = request.data.get('subject')
        tasks_count = request.data.get('tasks_count')

        try:
            tasks_count = int(tasks_count)
        except (TypeError, ValueError):
            return Response(
                {'error': 'Поле tasks_count должно быть целым числом'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if tasks_count <= 0:
            return Response(
                {'error': 'tasks_count должен быть больше 0'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        available_tasks = Task.objects.filter(subject=subject)
        if not available_tasks.exists():
            return Response(
                {'error': 'Нет задач по выбранному предмету'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        selected_tasks = random.sample(list(available_tasks), min(tasks_count, available_tasks.count()))
        session = TrainingSession.objects.create(
            user=request.user,
            subject=subject,
            total_tasks=len(selected_tasks),
            task_ids=[task.id for task in selected_tasks],
        )

        first_task = selected_tasks[0]
        return Response(
            {
                'session_id': session.id,
                'subject': subject,
                'total_tasks': session.total_tasks,
                'current_task_index': 1,
                'task': {
                    'id': first_task.id,
                    'text': first_task.text,
                    'topic': first_task.topic,
                    'difficulty': first_task.difficulty,
                    'hints': first_task.hints,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class SubmitTrainingAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_id = request.data.get('session_id')
        task_id = request.data.get('task_id')
        user_answer = str(request.data.get('answer', '')).strip()

        if not session_id or not task_id or user_answer == '':
            return Response(
                {'error': 'Укажите session_id, task_id и answer'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = get_object_or_404(TrainingSession, id=session_id, user=request.user)

        if session.is_finished:
            return Response(
                {'error': 'Тренировка уже завершена'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        expected_task_id = session.task_ids[session.current_position]
        if int(task_id) != expected_task_id:
            return Response(
                {'error': 'Нарушен порядок задач в тренировке'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task = get_object_or_404(Task, id=task_id)
        is_correct = user_answer == task.correct_answer.strip()

        TrainingAnswer.objects.create(
            session=session,
            task=task,
            user_answer=user_answer,
            is_correct=is_correct,
        )

        profile = request.user.profile
        profile.solved_tasks += 1
        if is_correct:
            profile.correct_answers += 1
        profile.save()

        TaskAttempt.objects.create(
            user=request.user,
            task=task,
            is_correct=is_correct,
            subject=task.subject,
            difficulty=task.difficulty,
        )

        session.current_position += 1
        if is_correct:
            session.correct_answers += 1

        has_next = session.current_position < session.total_tasks
        if not has_next:
            session.is_finished = True
            session.finished_at = timezone.now()
        session.save()

        payload = {
            'correct': is_correct,
            'message': 'Верно!' if is_correct else 'Неверно.',
            'session_finished': session.is_finished,
            'progress': {
                'answered': session.current_position,
                'total': session.total_tasks,
            },
        }

        if has_next:
            next_task = Task.objects.get(id=session.task_ids[session.current_position])
            payload['next_task'] = {
                'id': next_task.id,
                'text': next_task.text,
                'topic': next_task.topic,
                'difficulty': next_task.difficulty,
                'hints': next_task.hints,
            }
            payload['current_task_index'] = session.current_position + 1
        else:
            payload['results'] = _build_results(session)

        return Response(payload, status=status.HTTP_200_OK)


class TrainingResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = get_object_or_404(TrainingSession, id=session_id, user=request.user)
        if not session.is_finished:
            return Response(
                {'error': 'Тренировка ещё не завершена'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(_build_results(session), status=status.HTTP_200_OK)


def _build_results(session: TrainingSession):
    answers = session.answers.select_related('task').all()
    return {
        'session_id': session.id,
        'subject': session.subject,
        'total_tasks': session.total_tasks,
        'correct_answers': session.correct_answers,
        'accuracy_percent': round((session.correct_answers / session.total_tasks) * 100, 2)
        if session.total_tasks
        else 0,
        'table': [
            {
                'task_id': answer.task.id,
                'task_text': answer.task.text,
                'user_answer': answer.user_answer,
                'correct_answer': answer.task.correct_answer,
                'is_correct': answer.is_correct,
            }
            for answer in answers
        ],
    }