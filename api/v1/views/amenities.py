#!/usr/bin/python3
"""View for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amall():
    """Retrieves all Amenity objects"""
    myList = []
    for Amenity in storage.all("Amenity").values():
        myList.append(Amenity.to_dict())
    return jsonify(myList)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def ameone(amenity_id):
    """Retrieves Amenity object by its ID"""
    valid = storage.get(Amenity, amenity_id)
    if valid is None:
        abort(404)
    return jsonify(valid.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def amdelete(amenity_id):
    """Deletes Amenity object by its ID """
    valid = storage.get(Amenity, amenity_id)
    if valid is None:
        abort(404)
    valid.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def amcreate():
    """Creates an Amenity object by POST"""
    req = request.get_json()
    if req is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)

    obj_Amenitys = Amenity(**req)
    obj_Amenitys.save()
    return make_response(jsonify(obj_Amenitys.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def Amenity_update(amenity_id):
    """Updates a Amenitys object by PUT"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, value)
        obj.save()
        return jsonify(obj.to_dict())
