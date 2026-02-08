"""
Custom Authentication Classes for FOSSEE Chemical Equipment Visualizer
Implements lenient token authentication that allows anonymous access
"""

from __future__ import annotations

from typing import Optional, Tuple
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.request import Request


class LenientTokenAuthentication(TokenAuthentication):
    """
    Token authentication that allows anonymous access.
    
    - If Authorization header present: validates token, returns user
    - If Authorization header missing: returns None (anonymous access)
    - If token invalid: raises AuthenticationFailed
    
    This allows endpoints to work for both authenticated and anonymous users,
    with views deciding how to handle each case.
    """
    
    def authenticate(self, request: Request) -> Optional[Tuple[User, Token]]:
        """
        Authenticate the request and return a tuple of (user, token) or None.
        
        Returns None for anonymous access (no header), allowing the view
        to proceed with request.user as AnonymousUser.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        # No auth header = anonymous access (return None, not error)
        if not auth_header:
            return None
        
        # Has auth header = validate token (may raise AuthenticationFailed)
        return super().authenticate(request)
    
    def authenticate_header(self, request: Request) -> str:
        """
        Return a string for WWW-Authenticate header.
        """
        return 'Token'


class OptionalTokenAuthentication(LenientTokenAuthentication):
    """
    Alias for LenientTokenAuthentication for clarity.
    Use in views that support both authenticated and anonymous users.
    """
    pass
