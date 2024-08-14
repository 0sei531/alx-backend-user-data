#!/usr/bin/env python3
""" End-to-End Integration Test
    This script tests user registration, login, profile access, logout,
    password reset token generation, and password update.
"""
import requests

BASE_URL = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test user registration. """
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/users', data=data)
    msg = {"email": email, "message": "user created"}
    assert response.status_code == 200, "Failed to register user"
    assert response.json() == msg, "Unexpected response for user registration"
    print("User registration successful.")


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test login with incorrect password. """
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    assert response.status_code == 401, "Expected 401 for wrong password"
    print("Login with wrong password correctly failed.")


def log_in(email: str, password: str) -> str:
    """ Test login with correct password. """
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    msg = {"email": email, "message": "logged in"}
    assert response.status_code == 200, "Failed to login"
    assert response.json() == msg, "Unexpected response for login"
    session_id = response.cookies.get("session_id")
    print("Login successful.")
    return session_id


def profile_unlogged() -> None:
    """ Test profile access without login. """
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403, "Expected 403 for no session"
    print("Profile access without login correctly denied.")


def profile_logged(session_id: str) -> None:
    """ Test profile access with valid session. """
    cookies = {"session_id": session_id}
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)
    msg = {"email": EMAIL}
    assert response.status_code == 200, "Failed to access profile with session"
    assert response.json() == msg, "Unexpected response for logged-in profile"
    print("Profile access with valid session successful.")


def log_out(session_id: str) -> None:
    """ Test logout. """
    cookies = {"session_id": session_id}
    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)
    assert response.status_code == 200, "Failed to log out"
    assert response.json() == {"message": "Bienvenue"}, "Unexpected response for logout"
    print("Logout successful.")


def reset_password_token(email: str) -> str:
    """ Test password reset token generation. """
    data = {"email": email}
    response = requests.post(f'{BASE_URL}/reset_password', data=data)
    assert response.status_code == 200, "Failed to get reset token"
    reset_token = response.json().get("reset_token")
    msg = {"email": email, "reset_token": reset_token}
    assert response.json() == msg, "Unexpected response for reset token"
    print("Password reset token generation successful.")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test password update. """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(f'{BASE_URL}/reset_password', data=data)
    msg = {"email": email, "message": "Password updated"}
    assert response.status_code == 200, "Failed to update password"
    assert response.json() == msg, "Unexpected response for password update"
    print("Password update successful.")


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
