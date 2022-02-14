from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserAccount
from .permissions import IsOwnerProfileOrReadOnly
# from .serializers import UserProfileSerializer
from django.contrib.auth import get_user_model

from ..tasker.serializers import UserInfoSerializer

User = get_user_model()


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerProfileOrReadOnly,]