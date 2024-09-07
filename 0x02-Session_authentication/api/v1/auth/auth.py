#!/usr/bin/env python3
"""auth.py module"""

import re
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

        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path and path in excluded_paths:
            return False
        if path and (path + "/") in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            regex_pattern = re.sub(r"\*", ".*", excluded_path)
            if re.fullmatch(regex_pattern, path):
                return False
            return True

        if path and path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header:  validate all requests to secure the API:
        Args:
            request (object, optional): Defaults to None.
        Returns:
            str: value of Authorized header
        """
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """_summary_

        Returns:
            _type_: _description_
        """
        return None
