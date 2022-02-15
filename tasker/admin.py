from django.contrib import admin
from tasker.models import *

# Register your models here.
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Rating)
