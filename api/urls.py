from django.urls import path
from api.tasker.views import *
from api.accounts.views import UserProfileDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('task/create/', TaskView.as_view()),
    path('task/post/', TaskPaginationView.as_view()),
    path('task/<int:id>/', PostDetail.as_view()),
    path('task/uuid/<slug:uuid>/', PostUuid.as_view()),
    path('user/<id>/', UserProfileDetailView.as_view(), name="profile"),
    path('task/comments/', CommentsView.as_view()),
    path('task/comment/<int:id>/', CommentsChangeView.as_view()),
    path('task/user/<int:pk>/', TaskUserView.as_view()),
    path('task/comments/<int:pk>/', CommentsTaskView.as_view()),
    path('task/<int:pk>/like/', LikeView.as_view()),
    path('task/<int:pk>/favourite/', FavouriteView.as_view()),
    path('task/favourite/', FavouriteUserView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)