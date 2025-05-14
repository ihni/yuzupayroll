from app.extensions import db

class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    total_salary_budget = db.Column(db.Numeric(10, 2), nullable=False)
    budget_start_month = db.Column(db.Integer, default=1)
    budget_start_day= db.Column(db.Integer, default=1)
    budget_end_month = db.Column(db.Integer, default=12)
    budget_end_day = db.Column(db.Integer, default=31)