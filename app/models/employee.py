from app.extensions import db
from .timestampmixin import TimestampMixin
from .softdeletemixin import SoftDeleteMixin

class Employee(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)

    role_id = db.Column(
        db.Integer, 
        db.ForeignKey('roles.id'), 
        nullable=False
    )
    role = db.relationship('Role', backref='employees')