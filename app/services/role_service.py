from app.utils import get_logger
from app.extensions import db
from app.models import Role

logger = get_logger(__name__)

class RoleService:

    @staticmethod
    def create(name, hourly_rate):
        role = Role(name=name, hourly_rate=hourly_rate)
        db.session.add(role)
        db.session.commit()
        return role
    
    @staticmethod
    def get_all():
        return Role.query.all()
    
    @staticmethod
    def get_by_id(role_id):
        return Role.query.get(role_id)