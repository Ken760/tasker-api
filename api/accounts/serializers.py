from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from accounts.models import UserAccount
User = get_user_model()
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta():
        model = UserAccount
        fields = ('id', 'email', 'password', 'first_name', 'last_name',  'activity', 'nickname', 'joinedDate', 'favoriteIds', 'picture', 'username', 'fullname')