from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from pvp.models import Match

from .permissions import IsAdminUserStrict
from .serializers import (
    AdminMatchResultSerializer,
    AdminTaskSerializer,
    AdminUserSerializer,
    AdminUserUpdateSerializer,
    ExternalApiCheckSerializer,
)
from tasks.models import Task


class AdminUserListView(ListAPIView):
    permission_classes = [IsAdminUserStrict]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all().order_by('id')


class AdminUserDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAdminUserStrict]
    queryset = User.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return AdminUserUpdateSerializer
        return AdminUserSerializer


class AdminTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserStrict]
    serializer_class = AdminTaskSerializer
    queryset = Task.objects.all().order_by('id')


class AdminMatchResultsView(ListAPIView):
    permission_classes = [IsAdminUserStrict]
    serializer_class = AdminMatchResultSerializer
    queryset = Match.objects.select_related('task', 'player1', 'player2').all().order_by('-created_at')


class ExternalApiHealthCheckView(APIView):
    permission_classes = [IsAdminUserStrict]

    def post(self, request):
        serializer = ExternalApiCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']
        req = Request(url, method='GET')

        try:
            with urlopen(req, timeout=5) as response:
                return Response(
                    {
                        'url': url,
                        'status_code': response.status,
                        'reachable': 200 <= response.status < 400,
                    },
                    status=status.HTTP_200_OK,
                )
        except HTTPError as exc:
            return Response(
                {
                    'url': url,
                    'status_code': exc.code,
                    'reachable': False,
                    'error': str(exc),
                },
                status=status.HTTP_200_OK,
            )
        except URLError as exc:
            return Response(
                {
                    'url': url,
                    'status_code': None,
                    'reachable': False,
                    'error': str(exc.reason),
                },
                status=status.HTTP_200_OK,
            )
