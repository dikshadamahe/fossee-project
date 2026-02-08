"""
Authentication Serializers for FOSSEE Chemical Equipment Visualizer
Handles user registration, login, and profile serialization
"""

from __future__ import annotations

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration"""
    
    username = serializers.CharField(
        min_length=3,
        max_length=150,
        help_text="Unique username (3-150 characters)"
    )
    email = serializers.EmailField(
        help_text="Valid email address"
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Password (min 8 characters)"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Confirm password"
    )
    
    def validate_username(self, value: str) -> str:
        """Check username is unique"""
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value.lower()
    
    def validate_email(self, value: str) -> str:
        """Check email is unique"""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value.lower()
    
    def validate(self, data: dict) -> dict:
        """Validate password match and strength"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Passwords do not match"
            })
        
        # Validate password strength
        try:
            validate_password(data['password'])
        except Exception as e:
            raise serializers.ValidationError({
                'password': list(e.messages)
            })
        
        return data
    
    def create(self, validated_data: dict) -> User:
        """Create new user and return with token"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    username = serializers.CharField(
        help_text="Username or email"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Password"
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response"""
    
    token = serializers.CharField()
    user = UserSerializer()
    message = serializers.CharField(required=False)


class ErrorSerializer(serializers.Serializer):
    """Serializer for error response"""
    
    error = serializers.CharField()
    details = serializers.DictField(required=False)
