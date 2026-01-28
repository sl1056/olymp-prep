from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
from users.models import Profile

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SubmitTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task_id = request.data.get('task_id')
        user_answer = request.data.get('answer', '').strip()

        if not task_id or user_answer == '':
            return Response(
                {"error": "Укажите task_id и answer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        task = get_object_or_404(Task, id=task_id)
        profile = request.user.profile
        is_correct = (user_answer == task.correct_answer.strip())

        profile.solved_tasks += 1
        if is_correct:
            profile.correct_answers += 1
        profile.save()

        return Response({
            "correct": is_correct,
            "task_id": task_id,
            "rating": profile.rating  # Elo рейтинг нужно добавить позже
        })