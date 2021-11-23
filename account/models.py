from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)

