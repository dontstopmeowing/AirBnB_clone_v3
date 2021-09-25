#!/usr/bin/python3
"""View for User objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def usall():
    """Retrieves all User objects"""
    myList = []
    for User in storage.all("User").values():
        myList.append(User.to_dict())
    return jsonify(myList)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET'])
def usone(user_id):
    """Retrieves User object by its ID"""
    valid = storage.get(User, user_id)
    if valid is None:
        abort(404)
    return jsonify(valid.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def usdelete(user_id):
    """Deletes User object by its ID """
    valid = storage.get(User, user_id)
    if valid is None:
        abort(404)
    valid.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def uscreate():
    """Creates an User object by POST"""
    req = request.get_json()
    if req is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "email" not in req:
        return make_response(jsonify({"error": "Missing email"}), 400)

    if "password" not in req:
        return make_response(jsonify({"error": "Missing password"}), 400)

    obj_Users = User(**req)
    obj_Users.save()
    return make_response(jsonify(obj_Users.to_dict()), 201)


@app_views.route('/users/<string:user_id>',
                 strict_slashes=False, methods=['PUT'])
def usupdate(user_id):
    """Updates a Users object by PUT"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj, key, value)
        obj.save()
        return jsonify(obj.to_dict())
