from rest_framework import serializers
from .models import PrayerRequestForm, BaptismRequestForm, DedicationForm, MembershipTransferForm, Events, BenevolenceForm, ContactForm, Announcements, Dependents

# Serializer classes for forms
class PrayerFormSerializer(serializers.ModelSerializer):
    """Prayer Form"""
    # Not required fields
    full_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.IntegerField(required=False, allow_null=True)

    # Required fields
    prayer_type = serializers.ChoiceField(choices=PrayerRequestForm.REQUEST_TYPE, default='personal request')
    prayer_request = serializers.CharField(required=True)

    class Meta:
        model = PrayerRequestForm
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'prayer_type',
            'prayer_request',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def to_representation(self, instance):
        """Ensure no null values are sent to frontend."""
        data = super().to_representation(instance)
        for key, value in data.items():
            if value is None:
                data[key] = ""
        return data


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
            'status',
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
            'status',
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


class DependentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependents
        fields = [
            'id',
            'name',
            'phone_number',
            'relationship',
        ]
        read_only_fields = ['id']


class BenevolenceSerializer(serializers.ModelSerializer):
    dependents = DependentsSerializer(many=True, required=False)

    class Meta:
        model = BenevolenceForm
        fields = [
            'id',
            'head_full_name',
            'head_phone_number',
            'email',
            'membership_status',
            'spouse_name',
            'church_name',
            'additional',
            'status',
            'created_at',
            'dependents'
        ]

    def create(self, validated_data):
        dependents_data = validated_data.pop('dependents', [])
        form = BenevolenceForm.objects.create(**validated_data)

        for dependent in dependents_data:
            Dependents.objects.create(benevolence_form=form, **dependent)

        return form

    def update(self, instance, validated_data):
        dependents_data = validated_data.pop('dependents', None)

        # update main BenevolenceForm fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # optionally update dependents if provided
        if dependents_data is not None:
            instance.dependents.all().delete()
            for dependent in dependents_data:
                Dependents.objects.create(benevolence_form=instance, **dependent)

        return instance


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = [
            'id',
            'title',
            'date',
            'venue',
            'description',
            'time',
            'department',
            'image',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class AnnouncementsSerializer(serializers.ModelSerializer):
    size = serializers.IntegerField(read_only=True)

    class Meta:
        model = Announcements
        fields = [
            'id',
            'title',
            'description',
            'size',
            'created_at'
        ]
        read_only_fields = ['id', 'size', 'created_at']

    
    def validate_file(self, value):
        """
        Validate that:
        - The uploaded file is a PDF.
        - The file size does not exceed 5 MB.
        """
        import os

        # ✅ Check file extension
        ext = os.path.splitext(value.name)[1].lower()
        if ext != '.pdf':
            raise serializers.ValidationError("Only PDF files are allowed.")

        # ✅ Check file content type (extra safety)
        if hasattr(value, 'content_type'):
            if value.content_type not in ['application/pdf']:
                raise serializers.ValidationError("Invalid file type. Only PDF files are accepted.")

        # ✅ Check file size limit
        max_size = 5 * 1024 * 1024  # 5 MB
        if value.size > max_size:
            raise serializers.ValidationError("File size must not exceed 5 MB.")

        return value