from django.urls import include, path
from api.tasker.views import (
    TaskView,
    # TaskerMainPage,
    TaskPaginationView,
    PostDetail,
    PostUuid,
    )
from api.accounts.views import UserProfileDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('task/create/', TaskView.as_view()),
    # path('task/post/', TaskerMainPage.as_view()),
    path('task/post/', TaskPaginationView.as_view()),
    path('task/<int:id>/', PostDetail.as_view()),
    path('task/uuid/<slug:uuid>/', PostUuid.as_view()),
    path("user/<userInfo_id>/", UserProfileDetailView.as_view(), name="profile"),
]

urlpatterns = format_suffix_patterns(urlpatterns)