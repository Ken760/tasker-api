from django.db.models import F, Sum, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework import mixins, generics
from rest_framework.views import APIView
from .serializers import (
    TaskCreateSerializer,
    CommentCreateSerializer,
    RatingSerializer,
    TaskMainPageSerializer,
    MyCursorPagination,
    CommentSerializer,
    )

from tasker.models import Task, Comment, Rating
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import filters

from ..accounts.permissions import IsOwnerProfileOrReadOnly, IsAuthorComment


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class TaskView(APIView):
    """Добавление Задач"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskCreateSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userInfo=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """Изменение и удаление постов"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = (IsOwnerProfileOrReadOnly, )
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskPaginationView(generics.ListAPIView):
    """Пагинация для задач"""
    queryset = Task.objects.get_queryset().order_by('-followings')
    serializer_class = TaskMainPageSerializer
    pagination_class = MyCursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('language', 'category', 'createdDate', 'difficult')
    search_fields = ['language', 'difficult', 'category', 'title', 'text']
    ordering_fields = '__all__'


class PostUuid(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """Чтение полной записи"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Task.objects.filter(pk=instance.id).update(followings=F('followings') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        for task in tasks:
            task.rating = task.ratings.aggregate(Avg('value'))['value__avg']
            task.save(update_fields=['rating',])
        return self.retrieve(request, *args, **kwargs)


class CommentsView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """Добавление Комментариев"""

    permission_classes = [IsAuthorComment]
    querysert = Comment.objects.filter()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(userInfo=self.request.user)


class CommentsChangeView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """Изменение и удаление комментариев"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorComment, )
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskUserView(generics.ListAPIView):
    """Фильтрация постов пользователя"""

    serializer_class = TaskCreateSerializer

    def get_queryset(self):
        return Task.objects.filter(
            userInfo_id=self.kwargs.get('pk')).select_related('userInfo')


class CommentsTaskView(generics.ListAPIView):
    """Получение комментариев по id поста"""

    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'

    def get_queryset(self):
        return Comment.objects.filter(
            taskId=self.kwargs.get('pk')).select_related('taskId').order_by('id')