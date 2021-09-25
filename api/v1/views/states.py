#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def state_all():
    """Retrieves all state objects"""
    myList = []
    for state in storage.all("State").values():
        myList.append(state.to_dict())
    return jsonify(myList)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_one(state_id):
    """Retrieves state object by its ID"""
    valid = storage.get(State, state_id)
    if valid is None:
        abort(404)
    return jsonify(valid.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def state_delete(state_id):
    """Deletes state object by its ID """
    valid = storage.get(State, state_id)
    if valid is None:
        abort(404)
    valid.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_create():
    """Creates a state object by POST"""
    req = request.get_json()
    if req is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)

    obj_states = State(**req)
    obj_states.save()
    return make_response(jsonify(obj_states.to_dict()), 201)


@app_views.route('/states/<string:state_id>',
                 strict_slashes=False, methods=['PUT'])
def state_update(state_id):
    """Updates a states object by PUT"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, value)
        obj.save()
        return jsonify(obj.to_dict())
