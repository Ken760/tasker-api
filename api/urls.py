from django.urls import include, path
from api.tasker.views import (
    TaskView,
    # TaskerMainPage,
    TaskPaginationView,
    PostDetail,
    PostUuid,
    )
from rest_framework.urlpatterns import format_suffix_patterns
from api.accounts.views import GithubLogin, GoogleLogin

urlpatterns = [
    path('task/create/', TaskView.as_view()),
    # path('task/post/', TaskerMainPage.as_view()),
    path('task/post/', TaskPaginationView.as_view()),
    path('task/<int:id>/', PostDetail.as_view()),
    path('task/uuid/<slug:uuid>/', PostUuid.as_view()),
    path('rest-auth/github/', GithubLogin.as_view(), name='github_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login')
]

urlpatterns = format_suffix_patterns(urlpatterns)