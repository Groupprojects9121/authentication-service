from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

from authapi.choices import CountryChoices, UserTypeChoices


class User(AbstractUser):  

    user_type = models.CharField(max_length=20, choices=UserTypeChoices.choices, default=UserTypeChoices.USER)
    country = models.CharField(max_length=2, choices=CountryChoices.choices, default=CountryChoices.INDIA)

    def __str__(self):
        return self.username


