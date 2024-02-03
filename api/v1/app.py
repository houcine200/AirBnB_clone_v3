#!/usr/bin/python3
"""Module defining the Flask application and API configuration."""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage_connection(exception):
    """Close the storage connection."""
    storage.close()


@app.errorhandler(404)
def not_found_error(err):
    response_error = {"error": "Not Found"}
    """returns a JSON-formatted 404 status code response."""
    return make_response(jsonify(response_error), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, debug=True, threaded=True)
