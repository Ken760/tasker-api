from rest_framework import serializers
from api.accounts.serializers import FullNameField
from tasker.models import Task, Comment, Rating
from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination
from rest_framework.relations import PrimaryKeyRelatedField
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    fullName = FullNameField(source='*')

    class Meta():
        model = User
        fields = ('id', 'activity', 'nickname', 'fullName')


class UserCommentSerializer(serializers.ModelSerializer):
    fullName = FullNameField(source='*')

    class Meta():
        model = User
        fields = ('id', 'fullName')


class CommentCreateSerializer(serializers.ModelSerializer):
    """Сериализация коментариев для создания"""
    userInfo = UserCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация коментариев для задач"""
    userInfo = UserCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'userInfo', 'text', 'createdDate')


class RatingSerializer(serializers.ModelSerializer):
    """Сериализация рейтинга"""

    class Meta:
        model = Rating
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализация задач"""
    comments = CommentSerializer(many=True)
    createdDate = serializers.DateTimeField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    userInfo = UserInfoSerializer(read_only=True)

    class Meta:
        model = Task
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

    class Meta:
        model = Task
        fields = ['id', 'title', 'language', 'category', 'difficult', 'text', 'theme', 'createdDate', 'updatedDate', 'uuid', 'followings']


class MyCursorPagination(LimitOffsetPagination):
    """Пагинация"""
    default_limit = 15
    page_size = 100
    max_page_size = 1000
