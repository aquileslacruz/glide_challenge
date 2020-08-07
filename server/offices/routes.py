from flask import request, abort, jsonify, current_app, json
from server.utilities import expand_data, get_list_url_parameters
from . import offices_blueprint

@offices_blueprint.route('', methods=['GET'], strict_slashes=False)
def get_offices():
    # Get URL parameters
    limit, offset, expand = get_list_url_parameters()

    # Get Data
    with open(current_app.config.get('OFFICES_JSON')) as json_file:
        office_data = json.load(json_file)

    # Filter data
    data = [e for e in office_data if e.get('id') > offset][:limit]

    # Expand data
    ALLOWED_EXPANSIONS = []
    if expand:
        data = expand_data(data, expand, ALLOWED_EXPANSIONS)

    return jsonify(data)

@offices_blueprint.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_office(id):
    # Get URL parameters
    expand = request.args.getlist('expand')

    # Get Data
    with open(current_app.config.get('OFFICES_JSON')) as json_file:
        office_data = json.load(json_file)

    # Filter data
    data = [e for e in office_data if e.get('id') == id]
    if len(data) == 0:
        abort(404, description='Id provided is invalid')

    # Expand data
    ALLOWED_EXPANSIONS = []
    if expand:
        data = expand_data(data, expand, ALLOWED_EXPANSIONS)

    return jsonify(data.pop())