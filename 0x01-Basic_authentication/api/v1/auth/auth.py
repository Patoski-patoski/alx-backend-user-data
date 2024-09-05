#!/usr/bin/env python3
"""auth.py module"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth: a class to manage the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth: define routes that don't need authentication
        Args:
            path (str): routes/url
            excluded_paths (List[str]): List of URL's
        Returns:
            bool: True or False
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path and path in excluded_paths:
            return False
        if path and (path + "/") in excluded_paths:
            return False
        if path and path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """_summary_
        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """_summary_

        Returns:
            _type_: _description_
        """
        return None
