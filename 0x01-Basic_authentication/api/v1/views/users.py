#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Returns:
      - List of all User objects in JSON format
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Returns:
      - User object in JSON format
      - 404 error if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Returns:
      - Empty JSON if the User has been correctly deleted
      - 404 error if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Returns:
      - User object in JSON format
      - 400 error if can't create the new User
    """
    try:
        req_json = request.get_json()
    except Exception:
        req_json = None
    
    if req_json is None:
        return jsonify({'error': "Wrong format"}), 400
    
    email = req_json.get("email", "")
    password = req_json.get("password", "")
    if not email:
        return jsonify({'error': "email missing"}), 400
    if not password:
        return jsonify({'error': "password missing"}), 400

    try:
        user = User(email=email, password=password)
        user.first_name = req_json.get("first_name")
        user.last_name = req_json.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Returns:
      - User object in JSON format
      - 404 error if the User ID doesn't exist
      - 400 error if can't update the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        req_json = request.get_json()
    except Exception:
        req_json = None
    
    if req_json is None:
        return jsonify({'error': "Wrong format"}), 400
    
    if req_json.get('first_name') is not None:
        user.first_name = req_json.get('first_name')
    if req_json.get('last_name') is not None:
        user.last_name = req_json.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
