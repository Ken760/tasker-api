from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from .serializers import (
    TaskCreateSerializer,
    CommentSerializer,
    RatingSerializer,
    TaskMainPageSerializer,
    MyCursorPagination,
    )

from tasker.models import Task, Comment, Rating
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class TaskView(APIView):
    """Добавление Задач"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskCreateSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskerMainPage(APIView):
    """Задачи на главной странице"""

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskMainPageSerializer(tasks, many=True)
        return Response(serializer.data)



class TaskPaginationView(ListAPIView):
    """Пагинация для задач"""
    queryset = Task.objects.get_queryset().order_by('id')
    serializer_class = TaskMainPageSerializer
    pagination_class = MyCursorPagination
    # ordering = 'id'
    # OrderingFilter = 'id'
    paginate_by = 5

