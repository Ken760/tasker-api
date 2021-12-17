from rest_framework import serializers
from rest_framework.response import Response

from tasker.models import Task, Comment, Rating
from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination
from rest_framework.relations import PrimaryKeyRelatedField
from drf_writable_nested.serializers import WritableNestedModelSerializer
from collections import OrderedDict

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
    comments = CommentSerializer(many=True)
    ratings = RatingSerializer(many=True)
    createdDate = serializers.DateTimeField(format="%d %b", read_only=True)

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
    """Короткий сериализатор задач для главной страницы"""
    createdDate = serializers.DateTimeField(format="%m.%d.%Y", read_only=True)
    text = CustomCharField(repr_length=100)

    class Meta:
        model = Task
        fields = ['id', 'title', 'language', 'category', 'difficult', 'text', 'theme', 'createdDate', 'updatedDate', 'uuid']


class MyCursorPagination(LimitOffsetPagination):
    """Курсорная пагинация"""
    default_limit = 3
    page_size = 10
    # page_query_param = 'page'
    # page_size_query_param = 'per_page'
    max_page_size = 1000
    ordering = 'id'



class MyCursorPagination(LimitOffsetPagination):
    """Курсорная пагинация"""

    default_limit = 2
    # limit_query_param = 'l'
    # offset_query_param = 'o'
    max_limit = 50