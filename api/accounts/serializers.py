from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from accounts.models import UserAccount
User = get_user_model()


class UserCreateSerializer(WritableNestedModelSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'activity', 'nickname')


class UserProfileSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'activity', 'nickname')