from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserAccount
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# class UserProfileListCreateView(ListCreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerProfileOrReadOnly,]