from django.shortcuts import render
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Create your views here.
