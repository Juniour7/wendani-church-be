from rest_framework import serializers
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

# Serializer classes for forms
class PrayerFormSerializer(serializers.ModelSerializer):
    class Meta:

        model = PrayerRequestForm
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'prayer_type',
            'prayer_request',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

