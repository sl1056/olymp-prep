from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Badge
from .serializers import BadgeProgressSerializer


class UserBadgesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        badges = Badge.objects.all().order_by('id')
        serializer = BadgeProgressSerializer(badges, many=True, context={'request': request})
        return Response(serializer.data)
