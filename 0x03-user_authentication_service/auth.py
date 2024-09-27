#!/usr/bin/env python3
"""
Auth model generating users
- register
- login
- valid log in
- 
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from typing import Optional
from sqlalchemy.util import NoneType
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """returned bytes of salted hash of the input password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Init the auth module"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Store new user in db if email not exists"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            self._db.add_user(email=email,
                              hashed_password=_hash_password(password))
        except ValueError as e:
            raise e

    def valid_login(self, email: str, password: str) -> bool:
        """Valid user in login"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """Find the user with the email, generate a new UUID and store it in
        the database as the user’s session_id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Takes a single `session_id` string argument and returns the
        corresponding `User` or None
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user’s session ID to None"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return

    def get_reset_password_token(self, email: str) -> str:
        """Generate a UUID and update the user’s reset_token database field"""
        if type(email) is not str or len(email) == 0:
            raise ValueError
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Find the corresponding user and update he's `hashed_password`"""
        if type(reset_token) is not str or len(reset_token) == 0:
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
