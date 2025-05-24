from app.extensions import db
from sqlalchemy import func
from enum import Enum as PyEnum

class PayrollStatusEnum(PyEnum):
    DRAFT = 'DRAFT'
    FINALIZED = 'FINALIZED'
    ARCHIVED = 'ARCHIVED'

    def __str__(self):
        return self.value

class Payroll(db.Model):
    __tablename__ = "payrolls"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    gross_pay = db.Column(db.Numeric(10, 2), nullable=False)
    net_pay = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(db.Enum(PayrollStatusEnum, name='payroll_status'),
                       nullable=False,
                       default=PayrollStatusEnum.DRAFT)
    
    archived_at = db.Column(db.DateTime, nullable=True)
    finalized_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime,
                           server_default=func.now(),
                           onupdate=func.now(),
                           nullable=False)

    employee = db.relationship('Employee', back_populates='payrolls')
    payroll_worklogs = db.relationship('PayrollWorklog', back_populates='payroll')