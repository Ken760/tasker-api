from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework.views import APIView

from .serializers import *
from tasker.models import Task, Comment, Like, Favourite
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import filters
from django.contrib.auth.mixins import LoginRequiredMixin
from ..accounts.permissions import IsOwnerProfileOrReadOnly, IsAuthorComment


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class TaskView(generics.CreateAPIView):
    """Добавление Задач"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def perform_create(self, serializer):
        serializer.save(userInfo=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """Изменение и удаление постов"""

    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = (IsOwnerProfileOrReadOnly, )
    lookup_field = 'id'


class TaskPaginationView(generics.ListAPIView):
    """Пагинация/фильтрация для задач"""
    queryset = Task.objects.get_queryset().order_by('-followings')
    serializer_class = TaskMainPageSerializer
    pagination_class = MyCursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('language', 'category', 'createdDate', 'difficult', 'isConfirmed')
    search_fields = ['language', 'difficult', 'category', 'title', 'text']
    ordering_fields = '__all__'


class PostUuid(generics.ListAPIView):
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
        return self.retrieve(request, *args, **kwargs)


class CommentsView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """Добавление Комментариев"""

    permission_classes = [IsAuthorComment]
    querysert = Comment.objects.filter()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(userInfo=self.request.user)


class CommentsChangeView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение и удаление комментариев"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorComment, )
    lookup_field = 'id'


class TaskUserView(generics.ListAPIView):
    """Получение постов пользователя"""

    serializer_class = TaskMainPageSerializer
    pagination_class = MyCursorPagination

    def get_queryset(self):
        return Task.objects.filter(
            userInfo_id=self.kwargs.get('pk')).select_related('userInfo')


class CommentsTaskView(generics.ListAPIView):
    """Получение комментариев по id поста"""

    serializer_class = CommentSerializer
    # pagination_class = MyCursorPagination

    def get_queryset(self):
        return Comment.objects.filter(
            taskId=self.kwargs.get('pk')).select_related('taskId').order_by('-createdDate')


class FavouriteUserView(generics.ListAPIView):
    """Получение избранных по id пользователя"""

    serializer_class = TaskMainPageSerializer
    pagination_class = MyCursorPagination
    permission_classes = [IsOwnerProfileOrReadOnly, ]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return ""
        return Task.objects.filter(favourites__userInfo=self.request.user)


class CollectionView(generics.ListAPIView):
    """Получение названия коллекций"""

    serializer_class = CollectionMainPageSerializer
    pagination_class = MyCursorPagination


class LikeView(generics.ListAPIView, generics.DestroyAPIView, mixins.DestroyModelMixin):
    """Добавление|Удаление лайков"""

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthorComment]

    def post(self, request, pk):
        if Like.objects.filter(userInfo=self.request.user, taskId=pk).exists():
            Like.objects.filter(userInfo=self.request.user, taskId_id=pk).delete()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Delete"
            })
        else:
            Like.objects.create(userInfo=self.request.user, taskId_id=pk)
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Create"
            })


class FavouriteView(generics.ListAPIView, generics.DestroyAPIView, mixins.DestroyModelMixin):
    """Добавление|Удаление избранных задач"""

    querysert = Favourite.objects.all()
    serializer_class = FavouriteAddSerializer
    permission_classes = [IsAuthorComment]

    def post(self, request, pk):
        if Favourite.objects.filter(userInfo=self.request.user, taskId=pk).exists():
            Favourite.objects.filter(userInfo=self.request.user, taskId_id=pk).delete()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Delete"
            })
        else:
            Favourite.objects.create(userInfo=self.request.user, taskId_id=pk)
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Create"
            })
