from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    phone = models.CharField(max_length=20, null=True)
    twilio_phone = models.CharField(max_length=20, null=True)
