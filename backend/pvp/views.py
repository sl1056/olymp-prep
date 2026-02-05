import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import QuizRoom
from tasks.models import Task


class CreateMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room = find_or_create_room(request.user)
        return Response({
            "match_id": room.id,
            "room_id": room.room_id,
            "waiting_for_opponent": room.player2 is None
        }, status=status.HTTP_201_CREATED)


class JoinMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, match_id):
        room = get_object_or_404(QuizRoom, id=match_id)
        
        if room.player1 == request.user:
            return Response({"error": "You are already in this match"}, status=status.HTTP_400_BAD_REQUEST)
        
        if room.player2 is not None:
            return Response({"error": "Match is already full"}, status=status.HTTP_400_BAD_REQUEST)
        
        room.player2 = request.user
        room.save()
        
        return Response({
            "match_id": room.id,
            "room_id": room.room_id,
            "joined": True
        })


class MatchStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, match_id):
        room = get_object_or_404(QuizRoom, id=match_id)
        
        return Response({
            "match_id": room.id,
            "room_id": room.room_id,
            "player1": room.player1.username,
            "player2": room.player2.username if room.player2 else None,
            "score_p1": room.score_p1,
            "score_p2": room.score_p2,
            "current_task_index": room.current_task_index,
            "is_active": room.is_active,
            "ready": room.player2 is not None
        })


def find_or_create_room(user):
    
    room = QuizRoom.objects.filter(player2__isnull=True, is_active=True).exclude(player1=user).first()
    
    if room:
        room.player2 = user
        room.save()
    else:
        room = QuizRoom.objects.create(
            room_id=str(uuid.uuid4())[:8],
            player1=user
        )
        random_tasks = Task.objects.order_by('?')[:5]
        room.tasks.set(random_tasks)
    
    return room