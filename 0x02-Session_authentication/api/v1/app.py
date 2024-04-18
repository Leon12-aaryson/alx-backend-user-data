#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


# Get the authentication type from environment variables
AUTH_TYPE = os.getenv("AUTH_TYPE")

# Set up authentication based on the chosen AUTH_TYPE
if os.getenv("AUTH_TYPE") == 'session_auth':
    from api.v1.auth.auth import SessionAuth
    auth = SessionAuth()
else:
    if AUTH_TYPE == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()
    elif AUTH_TYPE == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()


@app.before_request
def before_request():
    '''
    Function that helps filter requests
    '''
    if auth is not None:
        excluded_list = ['/api/v1/status/',
                         '/api/v1/unauthorized/',
                         '/api/v1/forbidden/',
                         '/api/v1/auth_session/login/']

        # Check if authentication is required for the request path
        if auth.require_auth(request.path, excluded_list):
            # Check if authorization header is missing
            if (auth.authorization_header(request) is None and
                    auth.session_cookie(request) is None):

                abort(401, description="Unauthorized")
            # Check if user is not authorized
            if auth.current_user(request) is None:
                abort(403, description='Forbidden')
    request.current_user = auth.current_user(request)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized access handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_access(error) -> str:
    """ Forbidden access handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
