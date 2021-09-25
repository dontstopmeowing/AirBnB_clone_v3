#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def plall(city_id):
    """Retrieves all Place objects"""
    if storage.get(City, city_id) is None:
        abort(404)

    places = storage.all("Place").values()
    myList = []
    for Place in places:
        if Place.city_id == city_id:
            myList.append(Place.to_dict())
    return jsonify(myList)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def plone(place_id):
    """Retrieves Place object by its ID"""
    valid = storage.get(Place, place_id)
    if valid is None:
        abort(404)
    return jsonify(valid.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def pldelete(place_id):
    """Deletes Place object by its ID """
    valid = storage.get(Place, place_id)
    if valid is None:
        abort(404)
    storage.delete(valid)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def plcreate(city_id):
    """Creates an Place object by POST"""
    if storage.get(City, city_id) is None:
        abort(404)

    if not request.get_json(silent=True):
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req = request.get_json()
    if "user_id" not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if storage.get(User, req["user_id"]) is None:
        abort(404)

    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)

    req['city_id'] = city_id
    obj_Places = Place(**req)
    obj_Places.save()
    return make_response(jsonify(obj_Places.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def plupdate(place_id):
    """Updates a Places object by PUT"""
    data = storage.get(Place, place_id)
    if data is None:
        abort(404)

    if not request.get_json(silent=True):
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()

    for key, value in req.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(data, key, value)
    data.save()
    return make_response(jsonify(data.to_dict()), 200)
