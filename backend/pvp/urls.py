from django.urls import path
from .views import CreateMatchView, JoinMatchView, MatchStatusView

urlpatterns = [
    # Compatibility HTTP endpoint: if websocket URL was built through Django urls.py
    # (e.g. /api/pvp/ws/<match_id>/), return clear instruction instead of generic 404.
    path('ws/<int:match_id>/', MatchStatusView.as_view(), name='pvp-ws-http-compat'),
    path('create/', CreateMatchView.as_view(), name='create-match'),
    path('join/<int:match_id>/', JoinMatchView.as_view(), name='join-match'),
    path('status/<int:match_id>/', MatchStatusView.as_view(), name='match-status'),
]
