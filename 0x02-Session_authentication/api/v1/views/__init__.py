#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint
from api.v1 import app
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import session_auth_bp


app_views = Blueprint("app_views", __name__,
                      url_prefix="/api/v1")


User.load_from_file()

# Register the session_auth blueprint
app.register_blueprint(session_auth_bp)
