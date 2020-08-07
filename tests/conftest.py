import json
import pytest
from server import create_app
from server.config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('test')
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

@pytest.fixture(scope='module')
def employee_data():
    with open(TestConfig.EMPLOYEES_JSON) as json_file:
        yield json.load(json_file)