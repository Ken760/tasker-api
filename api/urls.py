from django.urls import include, path
from api.tasker.views import (
    TaskView,
    # TaskerMainPage,
    TaskPaginationView,
    PostDetail,
    PostUuid,
    )
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('task/create/', TaskView.as_view()),
    # path('task/post/', TaskerMainPage.as_view()),
    path('task/post/', TaskPaginationView.as_view()),
    path('task/<int:id>/', PostDetail.as_view()),
    path('task/uuid/<slug:uuid>/', PostUuid.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)