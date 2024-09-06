#!/usr/bin/env python3
"""basic_auth.py module"""

import base64
import binascii
from typing import TypeVar
from api.v1.auth.auth import Auth


User = TypeVar("User")


class BasicAuth(Auth):
    """BasicAuth: class
    Args:
        Auth (class): Base class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extract_base64_authorization_header: extracts base64
        Args:
            authorization_header (str): header to be extracted
        Returns:
            str: returns the Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        after_basic = authorization_header.split("Basic")[1].strip()
        return after_basic

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """decode_base64_authorization_header: decoded value of a Base64 string
        Args:
            base64_authorization_header (str): authorization header
        Returns:
            str: the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            valid_base64 = base64.b64decode(base64_authorization_header)
            return valid_base64.decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """def extract_user_credentials: returns user mail and password
        Args:
            str (str): authorization header
        Return:
            str (tuple): (email and password)
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        find_seperator = decoded_base64_authorization_header.find(":")
        user_mail = decoded_base64_authorization_header[:find_seperator]
        user_passwd = decoded_base64_authorization_header[find_seperator+1:]

        return (user_mail, user_passwd)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> User:
        """user_object_from_credentials:
        Args:
            user_email (str): user email
            user_pwd (str): user password
        Return:
            User(instance) or None
        """
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        from models.user import User

        users = User()
        users = users.search({"email": user_email})
        if users:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None

    def current_user(self, request=None) -> User:
        """current_user: retrieves the current user

        Args:
            request (optional):. Defaults to None.
        Returns:
            User: User details
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        extract_header = self.extract_base64_authorization_header(auth_header)
        if extract_header is None:
            return None
        decode_header = self.decode_base64_authorization_header(extract_header)
        if decode_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decode_header)
        if user_pwd is None or user_email is None:
            return None
        user_cred = self.user_object_from_credentials(user_email, user_pwd)
        return user_cred
