from app.extensions import db
from sqlalchemy import func

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    role_id = db.Column(
        db.Integer, 
        db.ForeignKey('roles.id'), 
        nullable=False
    )
    role = db.relationship('Role', backref='employees')

    status = db.Column(
        db.Enum('ACTIVE', 'INACTIVE', 'TERMINATED', name='employee_status'),
        nullable=False,
        server_default=db.text("'ACTIVE'")
    )

    terminated_at = db.Column(db.DateTime, nullable=True)
    is_archived = db.Column(db.Boolean, nullable=False, server_default=db.text('0'))
    archived_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )