from rest_framework import serializers
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

class PrayerFormSerializer(serializers.ModelSerializer):
    """Prayer Request Serializer"""
    class Meta:
        model = PrayerRequestForm
        fields = ['id', 'full_name', 'email', 'phone_number', 'prayer_type', 'prayer_request', 'created_at']



class BaptismFormSerializer(serializers.ModelSerializer):
    """Baptismal Form Serializer"""
    class Meta:
        model = BaptismRequestForm
        fields = ['id', 'full_name', 'email', 'phone_number', 'date_of_birth', 'is_baptised', 'is_study', 'additional_information', 'created_at']


class DedicationFormSerializer(serializers.ModelSerializer):
    """Dedication Form Serializer"""
    class Meta:
        model = DedicationForm
        fields = '__all__'

class MemberFormSerializer(serializers.ModelSerializer):
    """Dedication Form Serializer"""
    class Meta:
        model = MembershipTransferForm
        fields = '__all__'

class EventsSerializer(serializers.ModelSerializer):
    """Events  Serializer"""
    class Meta:
        model = Events
        fields = '__all__'

class BenevolenceFormSerializer(serializers.ModelSerializer):
    """Bennevolence Form  Serializer"""
    class Meta:
        model = BenevolenceForm
        fields = '__all__'

class ContactFormSerializer(serializers.ModelSerializer):
    """Contact Us Form  Serializer"""
    class Meta:
        model = ContactForm
        fields = '__all__'

class AnnouncementsSerializer(serializers.ModelSerializer):
    """Announcements  Serializer"""
    class Meta:
        model = Announcements
        fields = '__all__'


