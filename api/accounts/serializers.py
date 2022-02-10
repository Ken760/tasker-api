from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from accounts.models import Profile, UserAccount
from tasker.models import *
from api.tasker.serializers import TaskCreateSerializer

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'activity', 'nickname')


class UserProfileSerializer(WritableNestedModelSerializer):
    task = TaskCreateSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'