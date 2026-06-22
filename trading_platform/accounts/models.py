from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=10000.00)
    is_verified = models.BooleanField(default=False)
