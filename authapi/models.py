from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

from authapi.choices import CountryChoices, UserTypeChoices
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings 


class User(AbstractUser):  

    user_type = models.CharField(max_length=20, choices=UserTypeChoices.choices, default=UserTypeChoices.USER)
    country = models.CharField(max_length=2, choices=CountryChoices.choices, default=CountryChoices.INDIA)

    def __str__(self):
        return self.username
    
    
    
 # to get AUTH_USER_MODEL

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"

    
    
    



