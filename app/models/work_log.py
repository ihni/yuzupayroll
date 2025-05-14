from app.extensions import db

class WorkLog(db.Model):
    __tablename__ = "work_logs"

    id = db.Column(db.Integer, primary_key=True)
    date_worked = db.Column(db.DateTime, nullable=False)
    hours_worked = db.Column(db.Numeric(4, 2), nullable=False)
    employee_id = db.Column(db.Integer, foreign_key=True)