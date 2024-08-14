#!/usr/bin/env python3

"""
User model that inherits from SQLAlchemy Base class.

This model defines a table named 'users' with the following columns:
- id: Primary key, integer
- email: Email address, string, not nullable
- hashed_password: Hashed password, string, not nullable
- session_id: Session identifier, string, nullable
- reset_token: Password reset token, string, nullable

The model is intended to be used in a database managed by SQLAlchemy ORM.
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """ SQLAlchemy model for the 'users' table. """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
