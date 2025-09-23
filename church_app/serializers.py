from rest_framework import serializers
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

class PrayerFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequestForm
        fields = '__all__'

class BaptismFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaptismRequestForm
        fields = '__all__'