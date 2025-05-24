from app.extensions import db
from sqlalchemy import func

class PayrollWorklog(db.Model):
    __tablename__ = "payroll_worklogs"

    id = db.Column(db.Integer, primary_key=True)

    payroll_id = db.Column(db.Integer,
                           db.ForeignKey('payrolls.id'),
                           nullable=False,
                           index=True)
    worklog_id = db.Column(db.Integer,
                           db.ForeignKey('worklogs.id'),
                           nullable=False,
                           index=True)

    hours_recorded = db.Column(db.Numeric(5, 2), nullable=False)
    snapshot_locked = db.Column(db.Boolean, nullable=False, server_default='0')
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    worklog = db.relationship('Worklog', back_populates='payroll_worklogs')
    payroll = db.relationship('Payroll', back_populates='payroll_worklogs')