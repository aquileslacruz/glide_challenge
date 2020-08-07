import json

def test_get_offices_no_parameters(test_client, office_data):
    response = test_client.get('/offices')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == len(office_data)

def test_get_offices_with_limit(test_client, office_data):
    response = test_client.get('/offices?limit=2')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 2
    assert data == office_data[:2]

def test_get_offices_with_bad_limit(test_client, office_data):
    response = test_client.get('/offices?limit=-1')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Limit must be greater than 0'

def test_get_offices_with_exceeded_limit(test_client, office_data):
    response = test_client.get('/offices?limit=1001')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Limit must be less than or equal to 1000'

def test_get_offices_with_offset(test_client, office_data):
    response = test_client.get('/offices?offset=1')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == len(office_data) - 1
    assert data == [e for e in office_data if e.get('id') > 1]

def test_get_offices_with_offset_bad(test_client, office_data):
    response = test_client.get('/offices?offset=-1')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Offset must be greater than or equal to 0'

def test_get_offices_bad_expand(test_client):
    response = test_client.get('/offices?expand=manager')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Unidentified expand parameter'

def test_get_office_no_parameters(test_client, office_data):
    response = test_client.get('/offices/1')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get('id') == 1

def test_get_office_bad_id(test_client):
    response = test_client.get('/offices/10000')
    data = json.loads(response.data)

    assert response.status_code == 404
    assert isinstance(data, dict)
    assert data.get('description') == 'Id provided is invalid'

def test_get_office_bad_expand(test_client):
    response = test_client.get('/offices/1?expand=manager')
    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get('description') == 'Unidentified expand parameter'