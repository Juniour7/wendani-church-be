from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PrayerFormSerializer, BaptismFormSerializer, DedicationFormSerializer, MemberFormSerializer, EventsSerializer, BenevolenceFormSerializer, ContactFormSerializer, AnnouncementsSerializer 
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

# Create your views here.
class PrayerFormAPIView(viewsets.ModelViewSet):
    queryset = PrayerRequestForm.objects.all()
    serializer_class = PrayerFormSerializer

class BaptismFormAPIView(viewsets.ModelViewSet):
    queryset = BaptismRequestForm.objects.all()
    serializer_class = BaptismFormSerializer


class DedicationFormAPIView(viewsets.ModelViewSet):
    queryset = DedicationForm.objects.all()
    serializer_class = DedicationFormSerializer

class MembershipFormAPIView(viewsets.ModelViewSet):
    queryset = MembershipTransferForm.objects.all()
    serializer_class = MemberFormSerializer

class BenevolenceFormAPIView(viewsets.ModelViewSet):
    queryset = BenevolenceForm.objects.all()
    serializer_class = BenevolenceFormSerializer

class ContactFormAPIView(viewsets.ModelViewSet):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer

class AnnouncementsAPIView(viewsets.ModelViewSet):
    queryset = Announcements.objects.all()
    serializer_class = AnnouncementsSerializer


class EventsAPIView(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [IsAuthenticated]


