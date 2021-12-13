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


class TaskMainPageSerializer(serializers.ModelSerializer):
    """Короткий сериализатор задач для главной страницы"""
    createdDate = serializers.DateTimeField(format="%m.%d.%Y", read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'language', 'category', 'difficult', 'text', 'createdDate']