from flask import Flask
from app.extensions import db
from app.config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # import routeres here:
    from app.routes import roles_bp
    from app.routes import home_bp
    from app.routes import employees_bp
    from app.routes import work_logs_bp
    from app.routes import payrolls_bp
    
    # register blueprints here:
    app.register_blueprint(home_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(work_logs_bp)
    app.register_blueprint(payrolls_bp)

    return app
