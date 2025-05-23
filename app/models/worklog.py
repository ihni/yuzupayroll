from app.extensions import db
from sqlalchemy import CheckConstraint

class Worklog(db.Model):
    __tablename__ = "worklogs"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    hours_worked = db.Column(db.Numeric(4, 2), nullable=False)

    status = db.Column(
        db.Enum("ACTIVE", "LOCKED", "ARCHIVED", name="worklog_status"),
        nullable=False,
        server_default="ACTIVE"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('employees.id'),
        nullable=False
    )
    employee = db.relationship('Employee', backref='worklogs')

    __table_args__ = (
        CheckConstraint('hours_worked >= 0', name='check_hours_positive'),
    )