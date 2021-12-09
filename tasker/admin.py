from django.contrib import admin
from accounts.models import UserAccount
from tasker.models import *

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Rating)
