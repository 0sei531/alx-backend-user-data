#!/usr/bin/env python3
''' Define UserSession class. '''
from models.base import Base

class UserSession(Base):
    ''' Extend behaviors of Base class for session authentication using a DB. '''

    def __init__(self, *args: list, **kwargs: dict):
        ''' Initialize class instance. '''
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    def __str__(self):
        ''' Return string representation of UserSession instance. '''
        return f"[UserSession] ({self.id}) user_id: {self.user_id} - session_id: {self.session_id}"

    def to_json(self):
        ''' Return dictionary representation of UserSession instance. '''
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'session_id': self.session_id
        }
