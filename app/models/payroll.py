from sqlalchemy import func
from app.extensions import db

class Payroll(db.Model):
    __tablename__ = "payrolls"

    id = db.Column(db.Integer, primary_key=True)
    pay_period_start = db.Column(db.DateTime(timezone=True), nullable=False)
    pay_period_end = db.Column(db.DateTime(timezone=True), nullable=False)
    gross_pay = db.Column(db.Numeric(10, 2), nullable=False)
    net_pay = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(
        db.Enum('DRAFT', 'FINALIZED', 'ARCHIVED', name='payroll_status'),
        nullable=False,
        server_default='DRAFT'
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    archived_at = db.Column(db.DateTime(timezone=True), nullable=True)
    finalized_at = db.Column(db.DateTime(timezone=True), nullable=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('employees.id'),
        nullable=False
    )
    employee = db.relationship('Employee', backref='payrolls')