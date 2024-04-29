from django.contrib import admin
from .models import *

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Notification)
admin.site.register(Saved)
