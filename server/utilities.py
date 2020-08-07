from werkzeug.exceptions import HTTPException
from flask import jsonify, json, abort
from server.config import BaseConfig
import requests

EXPAND_OPTIONS = ['manager', 'office', 'department', 'superdepartment']

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

# Function that is used to expand the data
# received from APIs to accomodate for the
# expansion paths provided
def expand_data(initial_data, expand):
    # Copy the initial data
    data = initial_data

    # Process each of the expansion paths
    # ex. 'manager.manager' and 'office.department'
    for expansion in expand:
        # Split the expansion path
        parameters = expansion.split('.')
        # Expand the data progressivly
        data = process_expansion(data, parameters)

    return data

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
