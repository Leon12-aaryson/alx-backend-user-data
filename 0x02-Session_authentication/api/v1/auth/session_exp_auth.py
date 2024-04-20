#!/usr/bin/env python3

"""module for advanced task 9
"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Authentication class with expiration """

    def __init__(self):
        """ Initialize SessionExpAuth """
        super().__init__()
        # Assign session_duration from environment variable SESSION_DURATION
        session_duration_str = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration_str)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a Session ID with expiration.

        Args:
            user_id: The ID of the user for whom the session is being created.

        Returns:
            str: The Session ID if created successfully, None otherwise.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create session dictionary
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get user ID for a Session ID with expiration.

        Args:
            session_id: The Session ID for which the user ID is requested.

        Returns:
            str: The User ID if the session is valid and active,
            None otherwise.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        user_id = session_dict.get('user_id')

        # Check session expiration
        if self.session_duration <= 0:
            return user_id

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_id
