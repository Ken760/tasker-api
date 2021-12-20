import instance as instance
from django.db.models import F, Sum
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework import mixins, generics
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


class PostDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """Изменение и удаление постов"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskerMainPage(APIView):
    """Задачи на главной странице"""

    def get(self, request, format=None):
        tasks = Task.objects.all().update(followings=F('followings') + 1)
        serializer = TaskMainPageSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskPaginationView(ListAPIView):
    """Пагинация для задач"""
    queryset = Task.objects.get_queryset().order_by('-createdDate')
    serializer_class = TaskMainPageSerializer
    pagination_class = MyCursorPagination
    # ordering = 'id'
    # OrderingFilter = 'id'
    # paginate_by = 5


class PostUuid(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """Изменение и удаление ссылок"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        """Чтение полной записи"""

        instance = self.get_object()
        Task.objects.filter(pk=instance.id).update(followings=F('followings') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)