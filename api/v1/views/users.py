#!/usr/bin/python3
"""Module containing API routes for User objects."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Get all User objects."""
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get a User object by id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a User object by id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a User object."""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a User object."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at', 'password']:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict())
