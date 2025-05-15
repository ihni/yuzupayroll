from app.extensions import db
from .timestampmixin import TimestampMixin

class WorkLog(db.Model, TimestampMixin):
    __tablename__ = "work_logs"

    id = db.Column(db.Integer, primary_key=True)
    date_worked = db.Column(db.DateTime, nullable=False)
    hours_worked = db.Column(db.Numeric(4, 2), nullable=False)

    employee_id = db.Column(
        db.Integer, 
        db.ForeignKey('employees.id'), 
        nullable=False
    )
    employee = db.relationship('Employee', backref='work_logs')