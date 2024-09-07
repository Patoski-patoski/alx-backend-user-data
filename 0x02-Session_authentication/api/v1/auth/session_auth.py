#!/usr/bin/env python3
"""session auth.py module"""

import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth: sub class inherits from Auth
    Args:
        Auth (class): Base class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id
        Args:
            user_id (str, optional): Defaults to None.
        Returns:
            str: sesssion id or None
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """create USERID based on session_id
        Args:
            session_id (str, optional):session ID, Defaults to None.
        Returns:
            str: returns a User ID based on a Session ID, orNone:
        """
        if session_id is None and not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
