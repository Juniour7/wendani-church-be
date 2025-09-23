from rest_framework import serializers
from .models import PrayerReqestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

class PrayerFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerReqestForm
        fields = '__all__'