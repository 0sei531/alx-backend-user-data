#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Authentication """

    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """Extracts the Base64 part from the Authorization header"""
        if isinstance(authorization_header, str) and authorization_header.startswith("Basic "):
            return authorization_header.split(" ", 1)[1]
        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """Decodes the Base64 string"""
        if isinstance(base64_authorization_header, str):
            try:
                decoded_bytes = base64.b64decode(base64_authorization_header.encode('utf-8'))
                return decoded_bytes.decode('utf-8')
            except (base64.binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (Optional[str], Optional[str]):
        """Extracts user email and password from the decoded string"""
        if isinstance(decoded_base64_authorization_header, str) and ':' in decoded_base64_authorization_header:
            parts = decoded_base64_authorization_header.split(':', 1)
            return parts[0], parts[1]
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[TypeVar('User')]:
        """Finds a user object from the email and password"""
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
                for user in users:
                    if user.is_valid_password(user_pwd):
                        return user
            except Exception:
                return None
        return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """Returns the current user based on the request"""
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        email, pwd = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(email, pwd)
