from rest_framework import serializers
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements

# Serializer classes for forms
class PrayerFormSerializer(serializers.ModelSerializer):
    """Prayer Form"""
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


class BaptismFormSerializer(serializers.ModelSerializer):
    """Baptism Form"""
    class Meta:
        model = BaptismRequestForm
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'date_of_birth',
            'is_baptised',
            'is_study',
            'additional_information',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']



class DedicationFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = DedicationForm
        fields = [
            'id',
            'child_full_name',
            'date_birth',
            'gender',
            'father_full_name',
            'father_email',
            'father_phone_number',
            'mother_full_name',
            'mother_email',
            'mother_phone_number',
            'additional_information',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipTransferForm
        fields = [
            'id',
            'email',
            'phone_number',
            'date_of_birth',
            'physical_address',
            'from_church_name',
            'from_district_name',
            'from_conference_name',
            'from_address',
            'to_church_name',
            'to_district_name',
            'to_conference_name',
            'to_address',
            'additional_notes',
            'board_minute_number',
            'first_reading_date',
            'second_reading_date',
            'business_number',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'subject',
            'message',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']