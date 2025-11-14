from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .managers import UserProfileManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractUser):
    ROLES_CHOICES = [
        ('admin', 'admin'),
        ('elder', 'elder'),
        ('treasurer', 'treasurer'),
    ]
    username = None
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLES_CHOICES, default='elder')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    must_change_password = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserProfileManager()

    def __str__(self):
        return f"{self.username} ({self.role})"