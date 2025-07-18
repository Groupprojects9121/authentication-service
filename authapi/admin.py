from django.contrib import admin
from authapi.models import User
from authapi.models import PasswordResetOTP

admin.site.register(PasswordResetOTP)

@admin.register(User)
class UserModelAdminForm(admin.ModelAdmin):
    pass
