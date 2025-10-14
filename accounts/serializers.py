from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password

# ---------DISPLAY LOGGED-IN USER PROFILES
class UserSerializer(serializers.ModelSerializer):
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
        read_only_fields = ['id', 'created_at']


# ------SUPERUSER CREATES ELDER ACCOUNTS

class ElderCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'full_name',
            'role',
            'phone_number',
            'email',
            'password',
            'created_at',
        ]
    
    def create(self,validated_data):
        password = validated_data.pop('password', None)
        user = UserProfile(**validated_data)

        # Set a default password if one is not provided
        user.set_password(password or "changeme123")
        user.must_change_password= True
        user.save()
        return user
    
    
# ------ELDERS TO CHANGE THEIR OWN PASSWORD

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=True, validators=[validate_password])