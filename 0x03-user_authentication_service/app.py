#!/usr/bin/env python3
""" Basic Flask app with user registration, login, logout, profile management,
    password reset functionality, and session management.
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ Return a welcome message. """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """ Register a new user.
        Expects:
            - email
            - password
        Returns:
            - 201 if user is created
            - 400 if email is already registered
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, description="Email and password are required.")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Log in a user and create a session.
        Expects:
            - email
            - password
        Returns:
            - 200 with session ID if login is successful
            - 401 if login credentials are invalid
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, description="Email and password are required.")

    if not AUTH.valid_login(email, password):
        abort(401, description="Invalid email or password.")

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Log out a user and destroy the session.
        Redirects to '/' if logout is successful.
        Returns:
            - 403 if session ID is invalid or user is not found
    """
    session_id = request.cookies.get('session_id')

    if not session_id or not AUTH.get_user_from_session_id(session_id):
        abort(403, description="Invalid session ID.")

    AUTH.destroy_session(session_id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ Retrieve the profile of the logged-in user.
        Returns:
            - 200 with user email if session is valid
            - 403 if session is invalid
    """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403, description="Invalid session ID.")

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ Generate a password reset token.
        Expects:
            - email
        Returns:
            - 200 with reset token if email is registered
            - 403 if email is not registered
    """
    email = request.form.get('email')

    if not email:
        abort(400, description="Email is required.")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403, description="Email not registered.")


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ Update the user's password.
        Expects:
            - email
            - reset_token
            - new_password
        Returns:
            - 200 if password is updated successfully
            - 400 if any field is missing
            - 403 if reset token is invalid
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(
            400,
            description=(
                "Email, reset token, and new password are required."
            )
        )

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403, description="Invalid reset token.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
