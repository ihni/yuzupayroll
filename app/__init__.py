from flask import Flask, render_template    # type: ignore
from sqlalchemy.exc import OperationalError # type: ignore
from app.extensions import db
from app.config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.errorhandler(OperationalError)
    def handle_db_connection_error(error):
        return render_template('errors/db_unavailable.html'), 503

    # import routers here:
    from app.routes import roles_bp
    from app.routes import home_bp
    from app.routes import employees_bp
    from app.routes import worklogs_bp
    from app.routes import payrolls_bp
    from app.routes import organization_bp
    
    # register blueprints here:
    app.register_blueprint(home_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(worklogs_bp)
    app.register_blueprint(payrolls_bp)
    app.register_blueprint(organization_bp)
    
    return app
