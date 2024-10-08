#!/usr/bin/env python3
''' Define SessionExpAuth class. '''
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    ''' Extend behavior of SessionAuth class for session expiry. '''

    def __init__(self):
        ''' Initialize instance of SessionExpAuth. '''
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        ''' Create session associated with specified user id. '''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        ''' Return user ID associated with session ID. '''
        if not session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        created_at = session_dict.get('created_at')
        if not created_at:
            return None
        expiry_time = created_at + timedelta(seconds=self.session_duration)
        if expiry_time < datetime.now():
            return None
        return session_dict.get('user_id')
