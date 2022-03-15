from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
User = get_user_model()
from tasker.models import Like, Favourite


def hasSelfLike(pk, user) -> bool:
    """Проверка лайкнул ли пользователь пост"""
    if not user.is_authenticated:
        return False
    likes = Like.objects.filter(userInfo=user, taskId=pk)
    return likes.exists()


def hasSelfBookmark(pk, user) -> bool:
    """Проверка добавлен ли пост в закладки у пользователят"""
    if not user.is_authenticated:
        return False
    favourites = Favourite.objects.filter(userInfo=user, taskId=pk)
    return favourites.exists()