from flask import Flask, json
from .config import DevConfig, TestConfig
from .utilities import handle_exception

CONFIG = {'dev': DevConfig, 'test': TestConfig}

def create_app(env='dev'):
    app = Flask(__name__)
    app.config.from_object(CONFIG[env])
    register_error_handling(app)
    register_blueprints(app)
    return app

def register_error_handling(app):
    app.register_error_handler(Exception, handle_exception)

def register_blueprints(app):
    from server.employees import employees_blueprint
    from server.offices import offices_blueprint
    from server.departments import departments_blueprint
    
    app.register_blueprint(employees_blueprint)
    app.register_blueprint(offices_blueprint)
    app.register_blueprint(departments_blueprint)