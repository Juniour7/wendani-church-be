from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to display the user information
    """
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'full_name',
            'role',
            'phone_number',
            'email',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only = True, validators=[validate_password] )
    password2 = serializers.CharField(required=True, write_only=True, help_text='Repeat Password')

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'full_name',
            'role',
            'phone_number',
            'email',
            'created_at',
        ]
    
    def create(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    
    def validate_email(self, value):
        """check whether email is already in use"""
        if UserProfile.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists")
        return value