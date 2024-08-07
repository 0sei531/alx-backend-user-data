#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if authentication is required for a given path
        Args:
            path (str): The path to check
            excluded_paths (List[str]): List of paths that do not require authentication
        Returns:
            bool: True if authentication is required, False otherwise
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True

        # Ensure all paths have a trailing slash for consistency
        if path[-1] != '/':
            path += '/'
        excluded_paths = [p if p[-1] == '/' else p + '/' for p in excluded_paths]

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method to retrieve the Authorization header from a request
        Args:
            request (Request): The request object
        Returns:
            str: The value of the Authorization header, or None if not present
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to retrieve the current user
        Args:
            request (Request): The request object
        Returns:
            User: The current user, or None if not authenticated
        """
        return None
