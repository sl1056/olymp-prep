from django.urls import path
from .views import CreateMatchView, JoinMatchView, MatchStatusView

urlpatterns = [
    path('create/', CreateMatchView.as_view(), name='create-match'),
    path('join/<int:match_id>/', JoinMatchView.as_view(), name='join-match'),
    path('status/<int:match_id>/', MatchStatusView.as_view(), name='match-status'),
]