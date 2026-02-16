from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminMatchResultsView,
    AdminTaskViewSet,
    AdminUserDetailView,
    AdminUserListView,
    ExternalApiHealthCheckView,
)

router = DefaultRouter()
router.register(r'tasks', AdminTaskViewSet, basename='admin-tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', AdminUserListView.as_view(), name='admin-users-list'),
    path('users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-users-detail'),
    path('matches/results/', AdminMatchResultsView.as_view(), name='admin-matches-results'),
    path('external-api/check/', ExternalApiHealthCheckView.as_view(), name='admin-external-api-check'),
]
