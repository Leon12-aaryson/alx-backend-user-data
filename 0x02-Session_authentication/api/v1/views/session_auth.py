#!/usr/bin/env python3
"""Module to deal with the session authentication
"""

from flask import request, jsonify, Blueprint, abort
from models.user import User
from api.v1.app import auth  # Import the auth object from api.v1.app
import os

# Create a Blueprint for session authentication routes
session_auth_bp = Blueprint('session_auth', __name__,
                            url_prefix='/auth_session')


@session_auth_bp.route('/login', methods=['POST'])
def login():
    """Handle user login for session authentication.

    Validates user credentials and creates a session ID upon successful login.

    Returns:
        JSON response with user data upon successful login.
        JSON response with error message and appropriate status code for
        invalid login attempts.
    """
    # Retrieve email and password from request form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password is missing
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user based on email
    user = User.search({'email': email})
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session ID for the user
    session_id = auth.create_session(user.id)

    # Return user data and set session ID as cookie
    response_data = user.to_json()
    response = jsonify(response_data)
    session_cookie_name = os.getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_cookie_name, session_id)

    return response

def logout():
    """Handle user logout by destroying the session.

    Returns:
        Empty JSON response with status code 200 upon successful logout.
        JSON response with error message and status code 404 if logout fails.
    """
    # Destroy the session
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
