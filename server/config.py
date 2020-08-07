import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    EMPLOYEE_API = 'https://rfy56yfcwk.execute-api.us-west-1.amazonaws.com/bigcorp/employees'
    SECRET_KEY = os.getenv('SECRET_KEY', 'secrey_key')
    OFFICES_JSON = os.path.join(BASEDIR, 'data/offices.json')
    DEPARTMENTS_JSON = os.path.join(BASEDIR, 'data/departments.json')
    DEBUG = False
    TESTING = False

class DevConfig(BaseConfig):
    DEBUG = True

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True