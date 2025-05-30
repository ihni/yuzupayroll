from flask import Flask, render_template        # type: ignore
from sqlalchemy.exc import OperationalError     # type: ignore
from jinja2 import Undefined, StrictUndefined   # type: ignore
from backend.extensions import db
from backend.config import Config

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))

def create_app():

    app = Flask(
        __name__,
        template_folder=os.path.join(FRONTEND_DIR, 'templates'),
        static_folder=os.path.join(FRONTEND_DIR, 'static')
    )
    app.config.from_object(Config)
    
    if app.config.get('JINJA_SILENT_UNDEFINED', True):
        app.jinja_env.undefined = Undefined
    else:
        app.jinja_env.undefined = StrictUndefined

    db.init_app(app)

    @app.errorhandler(OperationalError)
    def handle_db_connection_error(error):
        return render_template('errors/db_unavailable.html'), 503

    # import routers here:
    from backend.routes import roles_bp
    from backend.routes import home_bp
    from backend.routes import employees_bp
    from backend.routes import worklogs_bp
    from backend.routes import payrolls_bp
    from backend.routes import organization_bp
    from backend.routes import dashboard_bp
    
    # register blueprints here:
    app.register_blueprint(home_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(worklogs_bp)
    app.register_blueprint(payrolls_bp)
    app.register_blueprint(organization_bp)
    app.register_blueprint(dashboard_bp)
    
    return app
