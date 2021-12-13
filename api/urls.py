from django.urls import include, path
from api.tasker.views import (
    TaskView,
    TaskerMainPage
    )
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('task/create/', TaskView.as_view()),
    path('task/post/', TaskerMainPage.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)