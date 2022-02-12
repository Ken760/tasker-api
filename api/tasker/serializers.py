from rest_framework import serializers
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer
# from ..accounts.serializers import UserProfileSerializer
from tasker.models import Task, Comment, Rating
from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination
from rest_framework.relations import PrimaryKeyRelatedField
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class UserProfileSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'activity', 'nickname')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор коментариев"""

    class Meta:
        model = Comment
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор рейтинга"""

    class Meta:
        model = Rating
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор задач"""
    comments = CommentSerializer(many=True, read_only=True)
    createdDate = serializers.DateTimeField(format="%d.%m.%Y", read_only=True)
    rating = serializers.FloatField(read_only=True)
    userInfo = UserProfileSerializer(default=serializers.HiddenField())

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
    createdDate = serializers.DateTimeField(format="%d.%m.%Y", read_only=True)
    text = CustomCharField(repr_length=200)

    class Meta:
        model = Task
        fields = ['id', 'title', 'language', 'category', 'difficult', 'text', 'theme', 'createdDate', 'updatedDate', 'uuid', 'followings']


class MyCursorPagination(LimitOffsetPagination):
    """пагинация"""
    default_limit = 15
    page_size = 100
    max_page_size = 1000

