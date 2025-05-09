from flask import Flask
from app.extensions import db
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import roles_bp
    from app.routes import home_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(roles_bp)


    return app
