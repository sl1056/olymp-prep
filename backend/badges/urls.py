from django.urls import path
from .views import UserBadgesAPIView

urlpatterns = [
    path('badges/', UserBadgesAPIView.as_view(), name='user-badges'),
]