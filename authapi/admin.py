from django.contrib import admin
from authapi.models import User


@admin.register(User)
class UserModelAdminForm(admin.ModelAdmin):
    pass
