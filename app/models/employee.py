from app.extensions import db
from .timestampmixin import TimestampMixin

class Employee(db.Model, TimestampMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    role_id = db.Column(
        db.Integer, 
        db.ForeignKey('roles.id'), 
        nullable=False
    )
    role = db.relationship('Role', backref='employees')