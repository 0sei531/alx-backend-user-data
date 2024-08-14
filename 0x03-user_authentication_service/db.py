#!/usr/bin/env python3
"""
Database module for ORM with SQLAlchemy.

This module provides a `DB` class to manage a SQLite database for a `User` model.
It includes methods to add, find, and update users in the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """Database class for Object-Relational Mapping (ORM) with SQLAlchemy."""

    def __init__(self):
        """Initializes the database engine and session."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)  # Reset the database for fresh start
        Base.metadata.create_all(self._engine)  # Create tables
        self.__session = None

    @property
    def _session(self):
        """Creates and returns a database session if one does not exist."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The hashed password for the user.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to User attributes.

        Returns:
            User: The first User object that matches the filters.

        Raises:
            InvalidRequestError: If no keyword arguments are provided or invalid keys are used.
            NoResultFound: If no user matches the filters.
        """
        if not kwargs:
            raise InvalidRequestError("No keyword arguments provided.")

        valid_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_keys:
                raise InvalidRequestError(f"Invalid key '{key}' in kwargs.")

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found matching the criteria.")

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments corresponding to User attributes to update.

        Raises:
            ValueError: If an invalid key is provided in kwargs.
            NoResultFound: If no user is found with the given user_id.
        """
        user = self.find_user_by(id=user_id)

        valid_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_keys:
                raise ValueError(f"Invalid key '{key}' in kwargs.")

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
