from app.extensions import db

class Payroll(db.Model):
    __tablename__ = "payroll"

    id = db.Column(db.Integer, primary_key=True)
    pay_period_start = db.Column(db.DateTime, nullable=False)
    pay_period_end = db.Column(db.DateTime, nullable=False)
    gross_pay = db.Column(db.Numeric(10, 2), nullable=False)
    total_hours = db.Column(db.Numeric(5, 2), nullable=False)
    employee_id = db.Column(db.Integer, foreign_key=True)