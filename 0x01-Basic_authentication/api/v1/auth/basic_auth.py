#!/usr/bin/env python3
'''
Module defining the BasicAuth class for basic authentication.
'''
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar

from models.user import User

T = TypeVar('T')


class BasicAuth(Auth):
    '''
    Definition of the BasicAuth class, a subclass of Auth for basic
    authentication.
    '''
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization header.

        Returns None if:
        - authorization_header is None
        - authorization_header is not a string
        - authorization_header doesn’t start with "Basic "
         (with a space at the end)
        """
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None

        """ Check if authorization_header starts with "Basic "
        (with a space at the end)"""
        if not authorization_header.startswith("Basic "):
            return None

        # Extract the value after "Basic "
        base64_part = authorization_header[6:]
        return base64_part

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        Decodes the Base64 string base64_authorization_header.

        Args:
            base64_authorization_header (str): The Base64 string.

        Returns:
            str: The decoded value as UTF-8 string.

        Returns None if:
        - base64_authorization_header is None
        - base64_authorization_header is not a string
        - base64_authorization_header is not a valid Base64 (using try/except)
        """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None

        try:
            # Attempt to decode the Base64 string
            decoded_value = base64.b64decode(
                base64_authorization_header
                ).decode('utf-8')
            return decoded_value
        except base64.binascii.Error:
            # Return None if decoding fails (invalid Base64)
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 Authorization
        header.

        Args:
            decoded_base64_authorization_header (str): Decoded Base64
            Authorization header.

        Returns:
            tuple: A tuple containing user email and password.

        Returns (None, None) if:
        - decoded_base64_authorization_header is None
        - decoded_base64_authorization_header is not a string
        - decoded_base64_authorization_header doesn’t contain ':'
        """
        # Check if decoded_base64_authorization_header is None
        if decoded_base64_authorization_header is None:
            return (None, None)

        # Check if decoded_base64_authorization_header is not a string
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        # Check if decoded_base64_authorization_header doesn’t contain ':'
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        # Split the decoded value into user email and password at the first ':'
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the user object corresponding to the provided credentials.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            TypeVar('User'): The user object if found, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the provided request.

        Args:
            request (Optional): The Flask request object.

        Returns:
            TypeVar('User'): The current user object if authenticated,
            otherwise None.
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return None
