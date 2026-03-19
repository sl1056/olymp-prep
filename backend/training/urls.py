from django.urls import path

from .views import StartTrainingView, SubmitTrainingAnswerView, TrainingResultsView


urlpatterns = [
    path('start/', StartTrainingView.as_view(), name='training-start'),
    path('submit/', SubmitTrainingAnswerView.as_view(), name='training-submit'),
    path('results/<int:session_id>/', TrainingResultsView.as_view(), name='training-results'),
]