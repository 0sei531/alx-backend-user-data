#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route(
    '/auth_session/login',
    methods=['POST'],
    strict_slashes=False
)
def login():
    """ POST /auth_session/login
    Handle user login. 

    Returns:
        - 400 if email or password is missing
        - 404 if no user is found for the given email
        - 401 if the password is incorrect
        - JSON representation of the user if login is successful
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        found_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not found_users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in found_users:
        if user.is_valid_password(password):
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv("SESSION_NAME"), session_id)
            return response

    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def logout():
    """ DELETE /auth_session/logout
    Handle user logout.

    Returns:
        - 200 if logout is successful
        - 404 if the session could not be destroyed
    """
    if auth.destroy_session(request):
        return jsonify({}), 200

    abort(404)
