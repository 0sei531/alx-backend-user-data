#!/usr/bin/env python3
"""
Session Authentication module
"""
from typing import Optional
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session Authentication class inherits from Auth """

    user_id_by_session_id: dict[str, str] = {}

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """Creates a Session ID for a given user ID

        Args:
            user_id (str, optional): The user ID for which to create a session.

        Returns:
            Optional[str]: The created session ID or None if user_id is invalid.
        """
        if not isinstance(user_id, str) or not user_id:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: Optional[str] = None) -> Optional[str]:
        """Retrieves the user ID associated with a given session ID

        Args:
            session_id (str, optional): The session ID for which to retrieve the user ID.

        Returns:
            Optional[str]: The associated user ID or None if session_id is invalid.
        """
        if not isinstance(session_id, str) or not session_id:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> Optional[User]:
        """Returns the User instance based on the session cookie

        Args:
            request: The HTTP request containing the session cookie.

        Returns:
            Optional[User]: The User instance or None if no valid user is found.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id) if user_id else None

    def destroy_session(self, request=None) -> bool:
        """Deletes the session for the current user, effectively logging them out

        Args:
            request: The HTTP request containing the session cookie.

        Returns:
            bool: True if the session was successfully deleted, False otherwise.
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False
