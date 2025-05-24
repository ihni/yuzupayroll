from app.utils import get_logger
from app.extensions import db
from app.models import Role

logger = get_logger(__name__)

class RoleService:

    @staticmethod
    def create(name, rate):
        try:
            if Role.query.filter_by(name=name).first():
                logger.warning(f"Cannot create role {name}: Duplicate found")
                return None
            role = Role(name=name, rate=rate)
            db.session.add(role)
            db.session.commit()
            logger.info(f"Created role with id '{role.id}'")
            return role
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error creating role '{name}': {e}")
            raise
    
    @staticmethod
    def get_all():
        roles = Role.query.all()
        logger.info(f"Fetched {len(roles)} roles")
        return roles
    
    @staticmethod
    def get_by_id(role_id):
        role = Role.query.get(role_id)
        if role:
            logger.info(f"Found role id '{role_id}'")
        else:
            logger.info(f"No role found with id '{role_id}'")
        return role
    
    @staticmethod
    def get_by_name(name):
        role = Role.query.filter_by(name=name).first()
        if role:
            logger.info(f"Found role name '{name}'")
        else: 
            logger.info(f"No role found with name '{name}'")
        return role
    
    @staticmethod
    def update(role_id, name=None, rate=None):
        role = Role.query.get(role_id)
        if not role:
            logger.info(f"Update failed: No role found with id '{role_id}'")
            return None

        if not name and not rate:
            logger.info(f"Tried updating role id '{role_id}' with empty fields")
            return None

        if name and name != role.name:
            existing = Role.query.filter_by(name=name).first()
            if existing:
                logger.info(f"Update failed: Role '{name}' already in use")
                return None

        old_name = role.name
        old_rate = role.rate

        updates = {
            "name": name,
            "rate": rate,
        }

        for attr, value in updates.items():
            if value is not None:
                setattr(role, attr, value)

        try:
            db.session.commit()
            logger.info(f"Updated role id '{role_id}'")
            if name:
                logger.info(f"Name '{old_name} -> '{name}'")
            if rate:
                logger.info(f"Rate '${old_rate} -> '${rate}'")
            return role
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error updating role id '{role_id}'")
            raise

    @staticmethod
    def archive(role_id):
        role = Role.query.get(role_id)
        if not role:
            logger.info(f"Delete failed: No role found with id '{role_id}'")
            return False
        
        if role.employees and len(role.employees) > 0:
            logger.info(f"Delete failed: role id '{role_id}' is assigned to {len(role.employees)} employee(s)")
            return False

        try:
            db.session.delete(role)
            db.session.commit()
            logger.info(f"Deleted role id '{role_id}'")
            return True
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error deleting role id '{role_id}'")
            raise