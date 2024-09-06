#!/usr/bin/env python3
"""basic_auth.py module"""

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
