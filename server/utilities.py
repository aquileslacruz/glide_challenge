from werkzeug.exceptions import HTTPException
from flask import jsonify, json, abort, current_app, request
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

# Function to get the URL parameters for limit, offset and expand
def get_list_url_parameters():
    # Get limit parameter or set to default
    try:
        limit = int(request.args.get('limit'))
        if limit <= 0:
            abort(400, 'Limit must be greater than 0')
        elif limit > 1000:
            abort(400, 'Limit must be less than or equal to 1000')
    except HTTPException as e:
        raise
    except:
        limit = 100

    # Get offset parameter or set to default
    try:
        offset = int(request.args.get('offset'))
        if offset < 0:
            abort(400, 'Offset must be greater than or equal to 0')
    except HTTPException as e:
        raise
    except:
        offset = 0

    # Get expand parameter or set to []
    expand = request.args.getlist('expand')

    return limit, offset, expand

# Function that is used to expand the data
# received from APIs to accomodate for the
# expansion paths provided
def expand_data(initial_data, expand, allowed=EXPAND_OPTIONS):
    # Copy the initial data
    data = initial_data

    # Process each of the expansion paths
    # ex. 'manager.manager' and 'office.department'
    for expansion in expand:
        # Split the expansion path
        parameters = expansion.split('.')
        # Expand the data progressivly
        data = process_expansion(data, parameters, allowed)

    return data

def process_expansion(data, parameters, allowed):
    # Get parameter to process
    current_param = parameters.pop(0)

    # Process parameter and new data needed for expansion
    expansion_data = get_expansion_data(data, current_param, allowed)

    # Recursively keep checking for more expansions needed
    if len(parameters) > 0:
        expansion_data = process_expansion(expansion_data, parameters, allowed)

    # Order the data received in a dictionary for easy use
    ordered_data = {elem['id']: elem for elem in expansion_data}

    # Expand the elements of the data
    for element in data:
        if isinstance(element[current_param], dict):
            id_to_expand = element[current_param].get('id')
            element[current_param] = update_dictionary(element[current_param], ordered_data.get(id_to_expand, None))
        elif isinstance(element[current_param], int):
            id_to_expand = element[current_param]
            element[current_param] = ordered_data.get(id_to_expand, None)
    
    return data

def get_expansion_data(data, parameter, allowed):
    # Check that the parameter makes sense
    if parameter not in allowed:
        abort(400, description='Unidentified expand parameter')
    # ex. Exclude something like department.manager
    elif len(data) > 0 and parameter not in data[0].keys():
        abort(400, description='There was a problem with the expand argument')

    # Get the ids of the parameter to be expanded
    ids = [e[parameter] for e in data if e.get(parameter) is not None]
    # Check if ids are dict (could have been expanded before)
    if all([isinstance(i, dict) for i in ids]):
        ids = [e.get('id') for e in ids]
    ids = set(ids)

    # Do not waste time if there are no ids
    if len(ids) == 0:
        return []

    # If 'manager' consult the API for the ids
    if parameter == 'manager':
        response = requests.get(current_app.config.get('EMPLOYEE_API'), params={'id': ids})
        expansion_data = response.json()
    # If 'office' use the complete set of OFFICES
    elif parameter == 'office':
        with open(current_app.config.get('OFFICES_JSON')) as json_file:
            expansion_data = json.load(json_file)
    # If 'department' or 'superdepartment' use the complete DEPARTMENTS
    elif parameter in ['department', 'superdepartment']:
        with open(current_app.config.get('DEPARTMENTS_JSON')) as json_file:
            expansion_data = json.load(json_file)
    else:
        expansion_data = []

    return expansion_data

# An auxiliar function to make sure that we don't remove data already expanded
def update_dictionary(dict1, dict2):
    result = dict()
    for key in set(dict1.keys()).union(set(dict2.keys())):
        if not isinstance(dict1.get(key), dict):
            result[key] = dict2.get(key)
        else:
            result[key] = dict1.get(key)
    return result