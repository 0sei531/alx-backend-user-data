#!/usr/bin/env python3
"""
Module of Session Authentication with Database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session Database Authentication Class """

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session for the given user_id and stores it in the database.

        Args:
            user_id (str): The ID of the user for whom the session is created.

        Returns:
            str: The created session ID, or None if creation fails.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session in the database
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID for a given session ID from the database.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID, or None if
                invalid or expired.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})

        if not user_session:
            return None

        user_session = user_session[0]

        # Check if session is expired
        expired_time = user_session.created_at + timedelta(
            seconds=self.session_duration
        )
        if expired_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the session from the database based on the request.

        Args:
            request: The request object containing session information.

        Returns:
            bool: True if the session was successfully removed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        user_session = UserSession.search({'session_id': session_id})

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
