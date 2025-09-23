from django.shortcuts import render
from .serializers import PrayerFormSerializer, BaptismFormSerializer
from rest_framework import viewsets
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

# Create your views here.
class PrayerFormAPIView(viewsets.ModelViewSet):
    queryset = PrayerRequestForm.objects.all()
    serializer_class = PrayerFormSerializer

class BaptismFormAPIView(viewsets.ModelViewSet):
    queryset = BaptismRequestForm.objects.all()
    serializer_class = BaptismFormSerializer