from django.urls import path
from .views import (
    OverallStatsView,
    SubjectStatsView,
    DifficultyStatsView,
    RecentAttemptsView, SubjectsChartDataView, AccuracyChartDataView
)

urlpatterns = [
    path('overall/', OverallStatsView.as_view(), name='analytics-overall'),
    path('subjects/', SubjectStatsView.as_view(), name='analytics-subjects'),
    path('difficulty/', DifficultyStatsView.as_view(), name='analytics-difficulty'),
    path('recent/', RecentAttemptsView.as_view(), name='analytics-recent'),
    path('chart/subjects/', SubjectsChartDataView.as_view()),
    path('chart/accuracy/', AccuracyChartDataView.as_view()),
]