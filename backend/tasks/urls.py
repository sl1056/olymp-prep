from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubmitTaskView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('submit/', SubmitTaskView.as_view(), name='submit-task'),
]