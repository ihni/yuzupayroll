from flask import Flask, render_template # type: ignore
from .database import Database
from .config import (
    DATABASE_CONFIG,
    RECONNECTION_DELAY,
    CONNECTION_ATTEMPTS
)
db = Database(
    **DATABASE_CONFIG, 
    attempts=CONNECTION_ATTEMPTS, 
    delay=RECONNECTION_DELAY
)

def create_app():
    app = Flask(__name__)

    @app.route('/')

    def placeholder_dashboard():
        return render_template('layouts/test.html')
    
    return app