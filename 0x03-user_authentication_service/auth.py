#!/usr/bin/env python3
"""DB module"""

import bcrypt
import uuid
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """To hashed the user password
    Args:
        password (str): string to be hashed
    Returns:
        byte: hashed password in bytes
    """
    b_password = password.encode()
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(b_password, salt)
    return hashed_password


def _generate_uuid() -> str:
    """generate a strin representation of uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user: register_user using email and password
        Args:
            email (str): email
            password (str): password
        Returns:
            User: User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """To locate a user by valid email and password
        Args:
            email (str): email
            password (str): password
        Returns:
            bool: True if registered(valid), False otherwise
        """
        try:
            valid_user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), valid_user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates a session from uuid
        Args:
            email (str):
        Returns:
            str:  session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db._session.commit()
            return user.session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get_user_from_session_id
        Args:
            session_id (str): session id
        Returns:
            Union[User, None]:  returns the corresponding User or None.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy_session: Destroys a users session
        Args:
            user_id (int): user_id to the session_id
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return user.session_id

        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """get_reset_password_token
        Args:
            email (str): email
        Returns:
            str: user corresponding to the email
        """
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            self._db._session.commit()
            return user.reset_token
        except NoResultFound:
            raise ValueError(f"User with email {email} does not exist")

    def update_password(self, reset_token: str, password: str) -> None:
        """update_password
        Args:
            reset_token (str): reset_token argument
            password (str): password
        Returns:
            str: updated password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.password = _hash_password(password)
            self._db._session.commit()
        except NoResultFound:
            error_token = f"User with reset_token {reset_token} does not exist"
            raise ValueError(error_token)
