from app.extensions import db

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)