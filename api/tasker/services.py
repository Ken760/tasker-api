from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
User = get_user_model()
from tasker.models import Like


def is_fan(pk, user) -> bool:
    """Проверка лайкнул ли пользователь пост"""
    if not user.is_authenticated:
        return False
    likes = Like.objects.filter(userInfo=user, taskId=pk)
    return likes.exists()