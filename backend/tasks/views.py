from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Task
from .serializers import TaskSerializer

class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['subject', 'topic', 'difficulty']
    search_fields = ['text']
    ordering_fields = ['id', 'subject', 'difficulty']
    ordering = ['id']

class SubmitTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        task_id = request.data.get('task_id')
        user_answer = str(request.data.get('answer', '')).strip()

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

        message = "Верно!" if is_correct else "Неверно."

        return Response({
            "correct": is_correct,
            "message": message
        })