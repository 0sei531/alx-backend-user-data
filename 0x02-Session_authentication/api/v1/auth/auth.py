#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv

class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method for requiring authentication """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Add slash to all cases for consistency
        path = path.rstrip('/') + '/'
        
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/') + '/'
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method that handles authorization header """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates current user """
        return None

    def session_cookie(self, request=None):
        """ Return cookie value from request. """
        if request is None:
            return None
        cookie_key = getenv('SESSION_NAME')
        return request.cookies.get(cookie_key)
