from app.extensions import db
from enum import Enum as PyEnum
from sqlalchemy import func # type: ignore

class EmployeeStatusEnum(PyEnum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    ARCHIVED = 'ARCHIVED'

    def __str__(self):
        return self.value

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, index=True)

    status = db.Column(
        db.Enum(EmployeeStatusEnum, name='employee_status'),
        nullable=False,
        default=EmployeeStatusEnum.ACTIVE
    )
    
    archived_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(), 
        onupdate=func.now()
    )

    role = db.relationship('Role', back_populates='employees')
    worklogs = db.relationship('Worklog', back_populates='employee')
    payrolls = db.relationship('Payroll', back_populates='employee')