#!/usr/bin/env python3
"""session database
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.user import User
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session Authentication class with database storage """

    def create_session(self, user_id=None):
        """ Create a Session ID and store it in the database (UserSession).

        Args:
            user_id: The ID of the user for whom the session is being created.

        Returns:
            str: The Session ID if created successfully, None otherwise.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session in the database (UserSession)
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get user ID for a Session ID by querying the database
        (UserSession).

        Args:
       session_id: The Session ID for which the user ID is requested.

        Returns:
            str: The User ID if the session is valid and active,
            None otherwise.
        """
        if session_id is None:
            return None

        # Query UserSession model to get user_id based on session_id
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None:
            return None

        # Check session expiration
        if self.session_duration > 0:
            created_at = user_session.created_at
            expiration_time = created_at + \
                timedelta(seconds=self.session_duration)
            if expiration_time < datetime.now():
                return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroy the UserSession based on the Session
        ID from the request cookie.

        Args:
            request: The Flask request object containing
            the session cookie.
        Returns:
            bool: True if the session is successfully destroyed,
            False otherwise.
        """
        if request is None:
            return False

        # Get session ID from session cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Query UserSession model to get the user session
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None:
            return False

        # Delete the user session from the database
        user_session.delete()
        return True
