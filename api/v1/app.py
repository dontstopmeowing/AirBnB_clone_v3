#!/usr/bin/python3
"""App"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)
# allow all origins to all methods.
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_storage(self):
    """Method that closes the session."""
    storage.close()


@app.errorhandler(404)
def page_not_found(self):
    """Method that handles 404 errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    h = getenv("HBNB_API_HOST", "0.0.0.0")
    p = getenv("HBNB_API_PORT", 5000)
    app.run(debug=True, host=h, port=p, threaded=True)
