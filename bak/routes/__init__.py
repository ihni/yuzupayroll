from flask import Blueprint

from .roles_routes import roles_bp

def register_routes(app):
    app.register_blueprint(roles_bp)