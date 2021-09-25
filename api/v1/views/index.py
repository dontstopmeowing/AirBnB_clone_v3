#!/usr/bin/python3
"""New Index"""
from api.v1.views import app_views
from flask import jsonify
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


@app_views.route('/status')
def status():
    """Returns the current status."""

    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """return count objects"""
    name_classes = {'users': storage.count(User),
                    'places': storage.count(Place),
                    'states': storage.count(State),
                    'cities': storage.count(City),
                    'amenities': storage.count(Amenity),
                    'reviews': storage.count(Review)}

    return jsonify(name_classes)
