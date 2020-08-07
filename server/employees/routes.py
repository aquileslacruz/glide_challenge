from flask import request, abort, jsonify, json, current_app
from server.utilities import expand_data
from . import employees_blueprint
import requests

@employees_blueprint.route('/', methods=['GET'], strict_slashes=False)
def get_employees():
    # Get URL parameters
    limit, offset, expand = get_list_url_parameters()

    # Request Data from API
    payload = {'limit': limit, 'offset': offset}
    response = requests.get(current_app.config.get('EMPLOYEE_API'), params=payload)
    data = response.json()

    # Expand the data
    if expand:
        data = expand_data(data, expand)

    # Return response
    return jsonify(data)

@employees_blueprint.route('/<int:id>/', methods=['GET'], strict_slashes=False)
def get_employee(id):
    # Get URL parameter
    expand = request.args.getlist('expand')

    # Request Data from API
    payload = {'id': id}
    response = requests.get(current_app.config.get('EMPLOYEE_API'), params=payload)
    data = response.json()
    if len(data) == 0:
        abort(404, description='No employee found with the provided id')

    # Expand the data
    if expand:
        data = expand_data(data, expand)

    # Return response
    return jsonify(data.pop())

#
# AUXILIAR FUNCTIONS
#

def get_list_url_parameters():
    # Get limit parameter or set to default
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = 100

    # Get offset parameter or set to default
    try:
        offset = int(request.args.get('offset'))
    except:
        offset = 0

    # Get expand parameter or set to []
    expand = request.args.getlist('expand')

    return limit, offset, expand
