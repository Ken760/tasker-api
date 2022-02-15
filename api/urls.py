from django.urls import include, path, re_path
from api.tasker.views import (
    TaskView,
    TaskPaginationView,
    PostDetail,
    PostUuid,
    CommentsView,
    TaskUserView
    )
from api.accounts.views import UserProfileDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('task/create/', TaskView.as_view()),
    # path('task/post/', TaskerMainPage.as_view()),
    path('task/post/', TaskPaginationView.as_view()),
    path('task/<int:id>/', PostDetail.as_view()),
    path('task/uuid/<slug:uuid>/', PostUuid.as_view()),
    path('user/<id>/', UserProfileDetailView.as_view(), name="profile"),
    path('task/comments/', CommentsView.as_view()),
    path('task/comments/<int:id>/', CommentsView.as_view()),
    path('task/user/<int:pk>/', TaskUserView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)