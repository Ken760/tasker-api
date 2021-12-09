from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView
from .serializers import (
    TaskMainPageSerializer,
    CommentSerializer,
    RatingSerializer
    )

from tasker.models import Task, Comment, Rating
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class PostView(APIView):
    """Добавление Задач"""

    queryset = Task.objects.all()
    serializer_class = TaskMainPageSerializer

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskMainPageSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskMainPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
