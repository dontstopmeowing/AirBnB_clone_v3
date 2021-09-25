#!/usr/bin/python3
"""View for City"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.city import City
from flask import abort
from flask import make_response
from flask import request
from models.state import State


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def retrieve_all(state_id):
    """Retrieves the list of all City objects."""
    if state_id:
        valid = storage.get(State, state_id)
        if valid is None:
            abort(404)
        else:
            cities = storage.all(City).values()
            myList = []
            for city in cities:
                if city.state_id == state_id:
                    myList.append(city.to_dict())
            return jsonify(myList)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['GET'])
def retrieve_byid(city_id):
    """Retrieves a City object"""
    if city_id:
        valid = storage.get(City, city_id)
        if valid is None:
            abort(404)
        else:
            return jsonify(valid.to_dict())


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    if city_id:
        valid = storage.get(City, city_id)
        if valid is None:
            abort(404)
        else:
            storage.delete(valid)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def response_city(state_id):
    """Creates a City"""
    if state_id:
        valid = storage.get(State, state_id)
        if valid is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    req['state_id'] = state_id
    city = City(**req)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    if city_id:
        obj_cities = storage.get(City, city_id)
        if obj_cities is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj_cities, key, value)
        obj_cities.save()
        return make_response(jsonify(obj_cities.to_dict()), 200)
