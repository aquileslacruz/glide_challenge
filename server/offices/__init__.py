from flask import Blueprint

offices_blueprint = Blueprint('offices', __name__, url_prefix='/offices')

from . import routes