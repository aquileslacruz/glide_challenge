from flask import request, abort, jsonify, json
from server.config import BaseConfig
from . import employees_blueprint
import requests

EXPAND_OPTIONS = ['manager', 'office', 'department', 'superdepartment']

@employees_blueprint.route('/', methods=['GET'], strict_slashes=False)
def get_employees():
    # Get URL parameters
    limit, offset, expand = get_list_url_parameters()

    # Request Data from API
    payload = {'limit': limit, 'offset': offset}
    response = requests.get(BaseConfig.EMPLOYEE_API, params=payload)
    data = response.json()

    # Expand the data
    if expand:
        data = expand_data(data, expand)

    # Return response
    return jsonify(data)

@employees_blueprint.route('/<int:id>/', methods=['GET'], strict_slashes=False)
def get_employee(id):
    # Get URL parameter
    expand = request.args.getlist('expand', None)

    # Request Data from API
    payload = {'id': id}
    response = requests.get(BaseConfig.EMPLOYEE_API, params=payload)
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
        limit = int(request.args.get('limit'), 10)
    except:
        limit = 10

    # Get offset parameter or set to default
    try:
        offset = int(request.args.get('offset', 0))
    except:
        offset = 0

    # Get expand parameter or set to []
    expand = request.args.getlist('expand')

    return limit, offset, expand

def expand_data(employees, expand):
    # Copy the initial data
    employee_data = employees

    # Process each of the expansion paths
    # ex. 'manager.manager' and 'office.department'
    for expansion in expand:
        # Split the expansion path
        parameters = expansion.split('.')
        # Expand the data progressivly
        employee_data = process_expansion(employee_data, parameters)

    return employee_data

def process_expansion(data, parameters):
    # Get parameter to process
    current_param = parameters.pop(0)

    # Process parameter and new data needed for expansion
    expansion_data = get_expansion_data(data, current_param)

    # Recursively keep checking for more expansions needed
    if len(parameters) > 0:
        expansion_data = process_expansion(expansion_data, parameters)

    # Order the data received in a dictionary for easy use
    ordered_data = {elem['id']: elem for elem in expansion_data}

    # Expand the elements of the data
    for element in data:
        id_to_expand = element[current_param]
        element[current_param] = ordered_data.get(id_to_expand, None)
    
    return data

def get_expansion_data(data, parameter):
    # Check that the parameter makes sense
    if parameter not in EXPAND_OPTIONS:
        abort(400, description='Unidentified expand parameter')
    # ex. Exclude something like department.manager
    elif len(data) > 0 and parameter not in data[0].keys():
        abort(400, description='There was a problem with the expand argument')

    # Get the ids of the parameter to be expanded
    ids = set([e[parameter] for e in data if e.get(parameter) is not None])
    # Do not waste time if there are no ids
    if len(ids) == 0:
        return []

    # If 'manager' consult the API for the ids
    if parameter == 'manager':
        response = requests.get(BaseConfig.EMPLOYEE_API, params={'id': ids})
        expansion_data = response.json()
    # If 'office' use the complete set of OFFICES
    elif parameter == 'office':
        with open(BaseConfig.OFFICES_JSON) as json_file:
            expansion_data = json.load(json_file)
    # If 'department' or 'superdepartment' use the complete DEPARTMENTS
    elif parameter in ['department', 'superdepartment']:
        with open(BaseConfig.DEPARTMENTS_JSON) as json_file:
            expansion_data = json.load(json_file)
    else:
        expansion_data = []

    return expansion_data
