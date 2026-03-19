# badges/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Badge
from .serializers import BadgeProgressSerializer

class UserBadgesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        badges = Badge.objects.all()
        serializer = BadgeProgressSerializer(
            badges,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)