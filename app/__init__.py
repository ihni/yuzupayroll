from flask import Flask # type: ignore
from app.extensions import db
from app.config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

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
