from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    ROLES_CHOICES = [
        ('admin', 'admin'),
        ('elder', 'elder'),
    ]
    role = models.CharField(max_length=100, choices=ROLES_CHOICES, default='elder')
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.username} ({self.role})"