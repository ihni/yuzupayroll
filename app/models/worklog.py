from app.extensions import db
from sqlalchemy import func
from enum import Enum as PyEnum

class WorklogStatusEnum(PyEnum):
    ACTIVE = 'ACTIVE'
    LOCKED = 'LOCKED'
    ARCHIVED = 'ARCHIVED'

    def __str__(self):
        return self.value
    
class Worklog(db.Model):
    __tablename__ = "worklogs"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    hours_worked = db.Column(db.Numeric(4, 2), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)

    status = db.Column(db.Enum(WorklogStatusEnum, name="worklog_status"),
                       nullable=False,
                       default=WorklogStatusEnum.ACTIVE)

    archived_at = db.Column(db.DateTime, nullable=True)
    locked_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())

    employee = db.relationship('Employee', back_populates='worklogs')
    payroll_worklogs = db.relationship('PayrollWorklog', back_populates='worklog')