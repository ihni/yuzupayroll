from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_migrate import Migrate       # type: ignore
db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)