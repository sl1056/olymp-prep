from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserBadgeSerializer
from django.contrib.auth.models import User

class UserBadgesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        badges = user.badges.select_related('badge').all()
        serializer = UserBadgeSerializer(badges, many=True)
        return Response(serializer.data)