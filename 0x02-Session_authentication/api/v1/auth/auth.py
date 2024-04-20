#!/usr/bin/env python3
'''
Module defining the Auth class
'''
from flask import request
import os
from typing import List, TypeVar


class Auth:
    '''
    Class definition of the Auth
    '''

    def require_auth(
            self,
            path: str,
            excluded_paths: List[str]
            ) -> bool:
        '''
        Returns False - path and excluded_paths
        will be used later, now, you don't need
        to take care of them
        '''
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(str.strip, excluded_paths):
                pattern = ''
                if exclusion_path.endswith('*'):
                    pattern = exclusion_path[:-1]
                    if path.startswith(pattern):
                        return False
                elif exclusion_path.endswith('/'):
                    pattern = exclusion_path[:-1]
                    if path == pattern or path.startswith(pattern + '/'):
                        return False
                else:
                    pattern = exclusion_path
                    if path == pattern or path.startswith(pattern + '/'):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        '''
        Returns None - request will be the Flask
        request object
        '''
        return request.headers.get('Authorization') if request else None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Returns None - request will be the Flask request
        object
        '''
        return None

    def session_cookie(self, request=None) -> str:
        """ Get the value of the session cookie from the request
        """
        if request is None:
            return None
        # Get the session cookie name from environment variable
        session_cookie_name = os.getenv("SESSION_NAME", "_my_session_id")
        # Return the value of the cookie named session_cookie_name
        return request.cookies.get(session_cookie_name, None)
