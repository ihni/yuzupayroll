from app.extensions import db

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    role_id = db.column(db.Integer, foreign_key=True)