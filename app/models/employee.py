from app.extensions import db

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    role_id = db.Column(db.Integer, foreign_key=True)
    email = db.Column(db.String(45), unique=True, nullable=False)