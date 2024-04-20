#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint
# from api.v1 import app
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import session_auth_bp


app_views = Blueprint("app_views", __name__,
                      url_prefix="/api/v1")

# Delay import of app
def register_views(app):
    """
    function to sort out the issue of circular imports
    by importing some modules internally
    """
    from api.v1 import app as main_app
    from api.v1.views.users import User

    User.load_from_file()

    # Register the session_auth blueprint
    main_app.register_blueprint(session_auth_bp)

# api/v1/app.py

from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)

# Register views
app_views.register_views(app)
