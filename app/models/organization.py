from app.extensions import db
from sqlalchemy import func

class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    total_salary_budget = db.Column(db.Numeric(10, 2), nullable=False)

    budget_start_month = db.Column(db.Integer, nullable=False, server_default='1')
    budget_start_day = db.Column(db.Integer, nullable=False, server_default='1')
    budget_end_month = db.Column(db.Integer, nullable=False, server_default='12')
    budget_end_day = db.Column(db.Integer, nullable=False, server_default='31')

    tax_rate = db.Column(db.Numeric(5, 4), nullable=False, server_default='0.0000')

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, 
                           nullable=False, 
                           server_default=func.now(), 
                           onupdate=func.now())