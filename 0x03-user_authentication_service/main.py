#!/usr/bin/env python3
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """
    Register a new user with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.
    """
    url = f'{BASE_URL}/register'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the wrong password.

    Args:
        email (str): The email of the user.
        password (str): The wrong password.
    """
    url = f'{BASE_URL}/login'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log in with the given email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID.
    """
    url = f'{BASE_URL}/login'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    return response.json().get('session_id')


def profile_unlogged() -> None:
    """
    Check the profile of an unlogged user.
    """
    url = f'{BASE_URL}/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Check the profile of a logged-in user.

    Args:
        session_id (str): The session ID of the user.
    """
    url = f'{BASE_URL}/profile'
    headers = {'Authorization': f'Bearer {session_id}'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Log out the user.

    Args:
        session_id (str): The session ID of the user.
    """
    url = f'{BASE_URL}/logout'
    headers = {'Authorization': f'Bearer {session_id}'}
    response = requests.post(url, headers=headers)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Get the reset password token for the given email.

    Args:
        email (str): The email of the user.

    Returns:
        str: The reset password token.
    """
    url = f'{BASE_URL}/reset_password_token'
    data = {'email': email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password using the reset token.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset password token.
        new_password (str): The new password.
    """
    url = f'{BASE_URL}/update_password'
    data = {'email': email,
            'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
