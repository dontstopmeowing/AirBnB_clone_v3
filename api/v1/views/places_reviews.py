#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviewAll(place_id):
    """Retrieves all review objects"""
    if storage.get(Place, place_id) is None:
        abort(404)

    reviews = storage.all(Review).values()
    myList = []
    for review in reviews:
        if review.place_id == place_id:
            myList.append(review.to_dict())
    return jsonify(myList)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviewOne(review_id):
    """Retrieves a review object by its ID"""
    valid = storage.get(Review, review_id)
    if valid is None:
        abort(404)
    return jsonify(valid.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def ReviewDel(review_id):
    """Deletes Place object by its ID """
    valid = storage.get(Review, review_id)
    if valid is None:
        abort(404)
    storage.delete(valid)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createRev(place_id):
    """Creates a review object by POST"""
    if storage.get(Place, place_id) is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    req = request.get_json()
    if "user_id" not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if storage.get(User, req["user_id"]) is None:
        abort(404)

    if "text" not in req:
        return make_response(jsonify({"error": "Missing text"}), 400)

    req['place_id'] = place_id
    obj_rev = Review(**req)
    obj_rev.save()
    return make_response(jsonify(obj_rev.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def reviewUpdat(review_id):
    """Updates a Places object by PUT"""
    data = storage.get(Review, review_id)
    if data is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    ignored = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in req.items():
        if key not in ignored:
            setattr(data, key, value)
    data.save()
    return make_response(jsonify(data.to_dict()), 200)
