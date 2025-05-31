from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


class User(AbstractUser):

    class UserTypeChoices(models.TextChoices):
        USER = 'USER', 'USER'
        RESTAURANT_OWNER = 'RESTAURANT_OWNER', 'Restaurant Owner'
        DELIVERY_PARTNER = 'DELIVERY_PARTNER', 'Delivery Partner'

    
    user_type = models.CharField(max_length=20, choices=UserTypeChoices.choices, default=UserTypeChoices.USER)

