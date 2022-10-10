from rest_framework import serializers
from tasker.models import *
from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination
from rest_framework.relations import PrimaryKeyRelatedField
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from api.tasker import services


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'activity', 'fullname', 'joinedDate')


class UserCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'fullname')


class CommentCreateSerializer(serializers.ModelSerializer):
    """Сериализация коментариев для создания"""
    userInfo = UserCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация коментариев для задач"""
    userInfo = UserCommentSerializer(read_only=True)
    createdDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'userInfo', 'text', 'createdDate', 'updatedDate')


class LikeSerializer(serializers.ModelSerializer):
    """Сериализация лайков"""
    userInfo = UserCommentSerializer(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"


class FavouriteAddSerializer(serializers.ModelSerializer):
    """Сериализация добавление избранных задач"""
    userInfo = UserCommentSerializer(read_only=True)

    class Meta:
        model = Favourite
        fields = "__all__"


class CustomCharField(serializers.CharField):
    """Кастомный сериализатор для ограничения текста"""
    def __init__(self, repr_length, **kwargs):
        self.repr_length = repr_length
        super(CustomCharField, self).__init__(**kwargs)

    def to_representation(self, value):
        return super(CustomCharField, self).to_representation(value)[:self.repr_length]


class TaskMainPageSerializer(serializers.ModelSerializer):
    """Сериализатор задач для главной страницы"""
    createdDate = serializers.DateTimeField(read_only=True)
    text = CustomCharField(repr_length=200)
    commentsCount = serializers.IntegerField(source="get_count_comments", read_only=True)
    likeCount = serializers.IntegerField(source='get_count_likes', read_only=True)
    hasSelfLike = serializers.SerializerMethodField()
    hasSelfBookmark = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'language', ''
            'category', 'difficult', 'text',
            'theme', 'createdDate', 'updatedDate',
            'uuid', 'commentsCount', 'likeCount',
            'hasSelfLike', 'hasSelfBookmark'
        ]

    def get_hasSelfLike(self, obj) -> bool:
        """Проверяет, лайкнул ли `request.user` пост"""
        user = self.context.get('request').user
        return services.hasSelfLike(obj, user)

    def get_hasSelfBookmark(self, obj) -> bool:
        """Проверяет, добавил ли `request.user` пост в избранное"""
        user = self.context.get('request').user
        return services.hasSelfBookmark(obj, user)


class FavouriteReceivingSerializer(serializers.ModelSerializer):
    """Сериализация получения избранных задач"""

    class Meta:
        model = Favourite
        fields = ('id', 'taskId')


class CollectionMainPageSerializer(serializers.ModelSerializer):
    """Сериализация коллекций для отображения на главной странице"""

    class Meta:
        model = Collection
        fields = ('id', 'name')


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализация задач"""
    comments = CommentSerializer(many=True, read_only=True)
    createdDate = serializers.DateTimeField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    userInfo = UserInfoSerializer(read_only=True)
    # likes = LikeSerializer(many=True, read_only=True)
    # favourites = FavouriteAddSerializer(many=True, read_only=True)
    likeCount = serializers.IntegerField(source='get_count_likes', read_only=True)
    commentsCount = serializers.IntegerField(source="get_count_comments", read_only=True)
    hasSelfLike = serializers.SerializerMethodField()
    hasSelfBookmark = serializers.SerializerMethodField()
    recommendations = TaskMainPageSerializer(source='get_recommendations', many=True)

    class Meta:
        model = Task
        fields = "__all__"

    def get_hasSelfLike(self, obj) -> bool:
        """Проверяет, лайкнул ли `request.user` пост"""
        user = self.context.get('request').user
        return services.hasSelfLike(obj, user)

    def get_hasSelfBookmark(self, obj) -> bool:
        """Проверяет, добавил ли `request.user` пост в избранное"""
        user = self.context.get('request').user
        return services.hasSelfBookmark(obj, user)


class MyCursorPagination(LimitOffsetPagination):
    """Пагинация"""
    default_limit = 15
    page_size = 100
    max_page_size = 1000