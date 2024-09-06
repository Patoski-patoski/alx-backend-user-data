#!/usr/bin/env python3
"""basic_auth.py module"""

import base64
import binascii
from api.v1.auth.auth import Auth


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
        """_summary_
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

        user_mail, user_passwd = decoded_base64_authorization_header.split(":")
        return (user_mail, user_passwd)
