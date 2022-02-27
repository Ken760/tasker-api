from django.contrib import admin
from tasker.models import *
from accounts.models import *

# Register your models here.
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favourite)
admin.site.register(UserAccount)