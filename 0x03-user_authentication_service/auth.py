#!/usr/bin/env python3
""" Authentication Module """

import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
from typing import Union


def _hash_password(password: str) -> str:
    """ Takes in a password and returns a salted hash using bcrypt. """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Generates and returns a new UUID as a string. """
    return str(uuid4())


class Auth:
    """ Auth class to interact with the authentication database. """

    def __init__(self):
        """ Initializes an instance of DB to interact with the database. """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user with the provided email and password.

        If the email is already registered, raises a ValueError.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates the login credentials.

        Returns True if the password is correct, otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str
                       ) -> Union[str, None]:
        """ Creates a new session ID for the user and stores
        it in the database.

        Returns the session ID as a string, or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Retrieves a user from the database based on the session ID.

        Returns the User object or None if the session ID is invalid.
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys the user's session by setting the session ID to None. """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a reset password token and updates the user's record.

        Returns the reset token, or raises a ValueError
        if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError(
                f"No user found with email {email}")

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates the user's password using the provided reset token.

        Resets the password and invalidates the reset token.
        Raises a ValueError if the token is invalid.
        """
        if reset_token is None or password is None:
            raise ValueError("Reset token and password cannot be None")

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except NoResultFound:
            raise ValueError("Invalid reset token")
