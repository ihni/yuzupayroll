from backend.extensions import db
from sqlalchemy import func # type: ignore
from enum import Enum as PyEnum

class RoleStatusEnum(PyEnum):
    ACTIVE = 'ACTIVE'
    ARCHIVED = 'ARCHIVED'

    def __str__(self):
        return self.value

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    rate = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(
        db.Enum(RoleStatusEnum, name='role_status'),
        nullable=False,
        default=RoleStatusEnum.ACTIVE
    )
    
    archived_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    
    employees = db.relationship('Employee', back_populates='role')