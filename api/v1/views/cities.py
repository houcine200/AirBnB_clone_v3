#!/usr/bin/python3
"""Module containing API routes for City objects."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State, City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Get all City objects of a State."""
    list_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for city in state.cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Get a City object by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object by id."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a City object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_city = City(state_id=state_id, **data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict())
