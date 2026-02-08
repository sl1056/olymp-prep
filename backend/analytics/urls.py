from django.urls import path
from .views import (
    OverallStatsView,
    SubjectStatsView,
    DifficultyStatsView,
    RecentAttemptsView
)

urlpatterns = [
    path('overall/', OverallStatsView.as_view(), name='analytics-overall'),
    path('subjects/', SubjectStatsView.as_view(), name='analytics-subjects'),
    path('difficulty/', DifficultyStatsView.as_view(), name='analytics-difficulty'),
    path('recent/', RecentAttemptsView.as_view(), name='analytics-recent'),
]