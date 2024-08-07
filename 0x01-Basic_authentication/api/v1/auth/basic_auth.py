#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar, Tuple, Optional


class BasicAuth(Auth):
    """ Basic Authentication Class """

    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """ Extract Base64 Authorization Header
        Args:
            authorization_header (str): The authorization header string
        Returns:
            Optional[str]: The Base64 part of the authorization header or None
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """ Decodes the value of a base64 string
        Args:
            base64_authorization_header (str): The Base64 string to decode
        Returns:
            Optional[str]: The decoded Base64 string or None
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = b64decode(base64_authorization_header.encode('utf-8'))
            return decoded_bytes.decode('utf-8')
        except (TypeError, ValueError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        """ Extracts user credentials from a decoded Base64 string
        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string
        Returns:
            Tuple[Optional[str], Optional[str]]: The user email and password or None, None
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[TypeVar('User')]:
        """ Returns the User instance based on email and password
        Args:
            user_email (str): The user's email
            user_pwd (str): The user's password
        Returns:
            Optional[TypeVar('User')]: The User instance or None
        """
        if user_email is None or not isinstance(user_email, str) or user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None
        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """ Retrieves the User instance for a request
        Args:
            request (Request): The request object
        Returns:
            Optional[TypeVar('User')]: The User instance or None
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        encoded = self.extract_base64_authorization_header(auth_header)
        if not encoded:
            return None
        decoded = self.decode_base64_authorization_header(encoded)
        if not decoded:
            return None
        email, pwd = self.extract_user_credentials(decoded)
        if not email or not pwd:
            return None
        return self.user_object_from_credentials(email, pwd)
