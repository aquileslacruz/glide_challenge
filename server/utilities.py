from werkzeug.exceptions import HTTPException
from flask import jsonify, json

# Exception handler for HTTPExceptions
def handle_http_exception(e):
    return jsonify({
        'code': e.code,
        'name': e.name,
        'description': e.description
    }), e.code

# General Exception handler
def handle_exception(e):
    if isinstance(e, HTTPException):
        return handle_http_exception(e)

    return jsonify({
        'code': 500,
        'name': 'Internal Server Error',
        'description': 'An unexpected error occured in the server'
    }), 500
    