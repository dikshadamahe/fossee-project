"""
Authentication Views for FOSSEE Chemical Equipment Visualizer
Handles user registration, login, logout, and profile
"""

from __future__ import annotations

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from .auth_serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    TokenResponseSerializer,
    ErrorSerializer,
)


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Create new user account and return authentication token.
    """
    permission_classes = [AllowAny]
    
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                ErrorSerializer({
                    'error': 'Registration failed',
                    'details': serializer.errors
                }).data,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = serializer.save()
        
        # Create or get token
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response(
            TokenResponseSerializer({
                'token': token.key,
                'user': UserSerializer(user).data,
                'message': 'Registration successful'
            }).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    Authenticate user and return token.
    Accepts username or email for login.
    """
    permission_classes = [AllowAny]
    
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                ErrorSerializer({
                    'error': 'Invalid request',
                    'details': serializer.errors
                }).data,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Try to find user by username or email
        user = None
        
        # Check if input looks like email
        if '@' in username:
            try:
                user_obj = User.objects.get(email__iexact=username)
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(
                request,
                username=username,
                password=password
            )
        
        if user is None:
            return Response(
                ErrorSerializer({
                    'error': 'Invalid credentials',
                    'details': {'non_field_errors': ['Username or password is incorrect']}
                }).data,
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                ErrorSerializer({
                    'error': 'Account disabled',
                    'details': {'non_field_errors': ['This account has been disabled']}
                }).data,
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get or create token
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response(
            TokenResponseSerializer({
                'token': token.key,
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            }).data
        )


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Delete user's authentication token.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request) -> Response:
        # Delete the user's token
        try:
            request.user.auth_token.delete()
        except Exception:
            pass  # Token might not exist
        
        return Response(
            {'message': 'Logout successful'},
            status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    """
    GET /api/auth/user/
    Get current authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        return Response(UserSerializer(request.user).data)
