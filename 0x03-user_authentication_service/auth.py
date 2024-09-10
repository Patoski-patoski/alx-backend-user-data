#!/usr/bin/env python3
"""DB module"""

import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


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
