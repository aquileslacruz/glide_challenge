from flask import Blueprint

employees_blueprint = Blueprint('employees', __name__, url_prefix='/employees')

from . import routes