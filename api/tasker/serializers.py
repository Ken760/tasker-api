from rest_framework import serializers
from tasker.models import Task, Comment, Rating
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.relations import PrimaryKeyRelatedField
from drf_writable_nested.serializers import WritableNestedModelSerializer


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
        fields = ['id', 'title', 'language', 'category', 'difficult', 'text', 'theme', 'createdDate']


