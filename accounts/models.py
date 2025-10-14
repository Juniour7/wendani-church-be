from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserProfileManager

# Create your models here.
class UserProfile(AbstractUser):
    ROLES_CHOICES = [
        ('admin', 'admin'),
        ('elder', 'elder'),
    ]
    username = models.CharField(max_length=1 ,blank=True, null=True, unique=False)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLES_CHOICES, default='elder')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserProfileManager()

    def __str__(self):
        return f"{self.username} ({self.role})"