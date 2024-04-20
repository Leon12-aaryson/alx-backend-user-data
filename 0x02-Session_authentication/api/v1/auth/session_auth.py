#!/usr/bin/env python3
"""module to deal with session authentication
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a Session ID using uuid
        session_id = str(uuid.uuid4())

        # Store the user_id mapped to the session_id
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve user_id based on session_id
        return self.user_id_by_session_id.get(session_id)

    def destroy_session(self, request=None):
        """Delete the user session / logout.

        Args:
            request: The Flask request object.

        Returns:
            True if the session is successfully destroyed, False otherwise.
        """
        if request is None:
            return False

        # Check if the request contains the Session ID cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Check if the Session ID is linked to any User ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        # Delete the Session ID from the dictionary
        del self.user_id_by_session_id[session_id]
        return True
