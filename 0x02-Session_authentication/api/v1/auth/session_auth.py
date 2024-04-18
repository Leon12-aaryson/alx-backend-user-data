#!/usr/bin/env python3
"""module to deal with session authentication
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Authentication class
    """
    pass
