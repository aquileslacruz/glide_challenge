import json

def test_get_departments_no_parameters(test_client, department_data):
    response = test_client.get('/departments')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == len(department_data)

def test_get_departments_with_limit(test_client, department_data):
    response = test_client.get('/departments?limit=2')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 2
    assert data == department_data[:2]

def test_get_departments_with_bad_limit(test_client, department_data):
    response = test_client.get('/departments?limit=-1')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Limit must be greater than 0'

def test_get_departments_with_exceeded_limit(test_client, department_data):
    response = test_client.get('/departments?limit=1001')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Limit must be less than or equal to 1000'

def test_get_departments_with_offset(test_client, department_data):
    response = test_client.get('/departments?offset=1')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == len(department_data) - 1
    assert data == [e for e in department_data if e.get('id') > 1]

def test_get_departments_with_offset_bad(test_client, department_data):
    response = test_client.get('/departments?offset=-1')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Offset must be greater than or equal to 0'

def test_get_departments_expand_superdepartment(test_client, department_data):
    response = test_client.get('/departments?expand=superdepartment')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == len(department_data)
    assert isinstance(data[0], dict)
    assert isinstance(data[0].get('superdepartment'), dict)

def test_get_departments_expand_superdepartment_twice(test_client, department_data):
    response = test_client.get('/departments?expand=superdepartment.superdepartment')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == len(department_data)
    assert isinstance(data[0], dict)
    assert isinstance(data[0].get('superdepartment'), dict)
    assert isinstance(data[0].get('superdepartment').get('superdepartment'), dict)

def test_get_departments_bad_expand(test_client):
    response = test_client.get('/departments?expand=manager')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Unidentified expand parameter'

def test_get_department_no_parameters(test_client):
    response = test_client.get('/departments/1')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get('id') == 1

def test_get_department_bad_id(test_client):
    response = test_client.get('/departments/10000')
    data = json.loads(response.data)

    assert response.status_code == 404
    assert isinstance(data, dict)
    assert data.get('description') == 'Id provided is invalid'

def test_get_department_expand_superdepartment(test_client):
    response = test_client.get('/departments/1?expand=superdepartment')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert isinstance(data.get('superdepartment'), dict)

def test_get_department_expand_superdepartment_twice(test_client):
    response = test_client.get('/departments/1?expand=superdepartment.superdepartment')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert isinstance(data.get('superdepartment'), dict)
    assert isinstance(data.get('superdepartment').get('superdepartment'), dict)

def test_get_office_bad_expand(test_client):
    response = test_client.get('offices/1?expand=manager')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Unidentified expand parameter'