from flask import request, abort, jsonify, current_app, json
from server.utilities import expand_data, get_list_url_parameters
from . import departments_blueprint

@departments_blueprint.route('', methods=['GET'], strict_slashes=False)
def get_departments():
    # Get URL parameters
    limit, offset, expand = get_list_url_parameters()

    # Get Data
    with open(current_app.config.get('DEPARTMENTS_JSON')) as json_file:
        department_data = json.load(json_file)

    # Filter data
    data = [e for e in department_data if e.get('id') > offset][:limit]

    # Expand data
    ALLOWED_EXPANSIONS = ['superdepartment']
    if expand:
        data = expand_data(data, expand, ALLOWED_EXPANSIONS)

    return jsonify(data)

@departments_blueprint.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_department(id):
    # Get URL parameters
    expand = request.args.getlist('expand')

    # Get Data
    with open(current_app.config.get('DEPARTMENTS_JSON')) as json_file:
        department_data = json.load(json_file)

    # Filter data
    data = [e for e in department_data if e.get('id') == id]
    if len(data) == 0:
        abort(404, description='Id provided is invalid')

    # Expand data
    ALLOWED_EXPANSIONS = ['superdepartment']
    if expand:
        data = expand_data(data, expand, ALLOWED_EXPANSIONS)

    return jsonify(data.pop())