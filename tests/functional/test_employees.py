from flask import current_app
import requests_mock
import json

def test_get_list_no_parameters(test_client, employee_data):
    mock_data = filter_employee_data(employee_data)
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=mock_data)
        response = test_client.get('/employees')
        data = json.loads(response.data)

    assert len(data) == len(employee_data)
    assert mock_request.called
    assert mock_request.last_request.qs.get('limit') == ['100']
    assert mock_request.last_request.qs.get('offset') == ['0']

def test_get_list_with_limit(test_client, employee_data):
    mock_data = filter_employee_data(employee_data, limit=3)
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=mock_data)
        response = test_client.get('/employees?limit=3')
        data = json.loads(response.data)

    assert len(data) == 3
    assert mock_request.called
    assert mock_request.last_request.qs.get('limit') == ['3']

def test_get_list_with_offset(test_client, employee_data):
    mock_data = filter_employee_data(employee_data, offset=1)
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=mock_data)
        response = test_client.get('/employees?offset=1')
        data = json.loads(response.data)

    assert len(data) == len(employee_data) - 1
    assert mock_request.called
    assert mock_request.last_request.qs.get('limit') == ['100']
    assert mock_request.last_request.qs.get('offset') == ['1']

def test_get_list_with_expand_manager(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=employee_data)
        response = test_client.get('/employees?expand=manager')
        data = json.loads(response.data)

    assert len(data) == len(employee_data)
    assert mock_request.called
    assert mock_request.call_count == 2
    assert isinstance(data[0].get('manager'), dict)

def test_get_list_with_expand_manager_twice(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=employee_data)
        response = test_client.get('/employees?expand=manager.manager')
        data = json.loads(response.data)

    assert len(data) == len(employee_data)
    assert mock_request.called
    assert mock_request.call_count == 3
    assert isinstance(data[0].get('manager'), dict)
    assert isinstance(data[0].get('manager').get('manager'), dict)

def test_get_list_with_expand_office(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=employee_data)
        response = test_client.get('/employees?expand=office')
        data = json.loads(response.data)

    assert len(data) == len(employee_data)
    assert mock_request.called
    assert mock_request.call_count == 1
    assert isinstance(data[0].get('office'), dict)

def test_get_list_with_expand_department(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=employee_data)
        response = test_client.get('/employees?expand=department')
        data = json.loads(response.data)

    assert len(data) == len(employee_data)
    assert mock_request.called
    assert mock_request.call_count == 1
    assert isinstance(data[0].get('department'), dict)

def test_get_list_with_expand_department_superdepartment(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=employee_data)
        response = test_client.get('/employees?expand=department.superdepartment')
        data = json.loads(response.data)

    assert len(data) == len(employee_data)
    assert mock_request.called
    assert mock_request.call_count == 1
    assert isinstance(data[0].get('department'), dict)
    assert isinstance(data[0].get('department').get('superdepartment'), dict)

def test_get_list_with_bad_extend(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=employee_data)
        response = test_client.get('/employees?expand=departments')
        data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data['code'] == 400
    assert data['description'] == 'Unidentified expand parameter'

def test_get_list_with_bad_extend_order(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=employee_data)
        response = test_client.get('/employees?expand=department.office')
        data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data['code'] == 400
    assert data['description'] == 'There was a problem with the expand argument'

def test_get_employee_no_parameters(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=[employee_data[0]])
        response = test_client.get('/employees/1')
        data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get('id') == 1
    assert mock_request.called
    assert mock_request.last_request.qs.get('id') == ['1']

def test_get_employee_expand_manager(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get('{}?id=1'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[0]])
        mock_request.get('{}?id=2'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[1]])
        response = test_client.get('/employees/1?expand=manager')
        data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get('id') == 1
    assert isinstance(data.get('manager'), dict)
    assert mock_request.called
    assert mock_request.call_count == 2
    assert mock_request.last_request.qs.get('id') == ['2']

def test_get_employee_expand_manager_twice(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get('{}?id=1'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[0]])
        mock_request.get('{}?id=2'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[1]])
        mock_request.get('{}?id=3'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[2]])
        response = test_client.get('/employees/1?expand=manager.manager')
        data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get('id') == 1
    assert isinstance(data.get('manager'), dict)
    assert isinstance(data.get('manager').get('manager'), dict)
    assert mock_request.called
    assert mock_request.call_count == 3
    assert mock_request.last_request.qs.get('id') == ['3']

def test_get_employee_expand_office(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get('{}?id=1'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[0]])
        response = test_client.get('/employees/1?expand=office')
        data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get('id') == 1
    assert isinstance(data.get('office'), dict)

def test_get_employee_expand_department(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get('{}?id=1'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[0]])
        response = test_client.get('/employees/1?expand=department')
        data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get('id') == 1
    assert isinstance(data.get('department'), dict)

def test_get_employee_expand_department(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get('{}?id=1'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[0]])
        response = test_client.get('/employees/1?expand=department.superdepartment')
        data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get('id') == 1
    assert isinstance(data.get('department'), dict)
    assert isinstance(data.get('department').get('superdepartment'), dict)

def test_get_employee_bad_expand_parameter(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get('{}?id=1'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[0]])
        response = test_client.get('/employees/1?expand=departments')
        data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('code') == 400
    assert data.get('description') == 'Unidentified expand parameter'

def test_get_employee_bad_expand_order(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get('{}?id=1'.format(current_app.config.get('EMPLOYEE_API')), json=[employee_data[0]])
        response = test_client.get('/employees/1?expand=department.manager')
        data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('code') == 400
    assert data.get('description') == 'There was a problem with the expand argument'

def test_get_employee_bad_id(test_client, employee_data):
    with requests_mock.Mocker() as mock_request:
        mock_request.get(current_app.config.get('EMPLOYEE_API'), json=employee_data)
        response = test_client.get('/employees/one')
        data = json.loads(response.data)

    assert response.status_code == 404

#
# AUXILIARY FUNCTIONS
#
def filter_employee_data(data, ids=[], limit=None, offset=0):
    if len(ids) > 0:
        data = [e for e in data if e.get('id') in ids]
    
    if offset > 0:
        data = [e for e in data if e.get('id') > offset]

    if limit is not None:
        data = data[:limit]

    return data