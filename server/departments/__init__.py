from flask import Blueprint

departments_blueprint = Blueprint('departments', __name__, url_prefix='/departments')

from . import routes