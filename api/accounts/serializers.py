from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from drf_writable_nested import WritableNestedModelSerializer
from accounts.models import UserAccount
User = get_user_model()
from rest_framework import serializers


class FullNameField(serializers.Field):

    def to_representation(self, value):
        return value.get_full_name()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    fullName = FullNameField(source='*')

    class Meta():
        model = UserAccount
        fields = ('id', 'email', 'password', 'first_name', 'last_name',  'activity', 'nickname', 'fullName')