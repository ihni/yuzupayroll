from app.extensions import db
from app.models import Role, RoleStatusEnum
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from app.utils import get_logger

logger = get_logger(__name__)

class RoleService:

    @staticmethod
    def create(name: str, rate: float) -> Role | None:
        """Create a new role if name doesn't exist"""
        try:
            if Role.query.filter_by(name=name).first():
                logger.warning(f"Role '{name}' already exists")
                return None
            
            role = Role(name=name, rate=rate)
            db.session.add(role)
            db.session.commit()
            logger.info(f"Created role ID {role.id}")
            return role
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Error creating role '{name}': {str(e)}")
            raise
    
    @staticmethod
    def get_by_id(role_id):
        """Get role by ID"""
        role = Role.query.get(role_id)
        if role:
            logger.debug(f"Found role ID {role_id}")
        else:
            logger.warning(f"Role ID {role_id} not found")
        return role
    
    @staticmethod
    def get_by_name(name):
        """Get role by exact name match"""
        role = Role.query.filter_by(name=name).first()
        if role:
            logger.debug(f"Found role '{name}'")
        else:
            logger.debug(f"Role '{name}' not found")
        return role
    
    @staticmethod
    def get_all(status: RoleStatusEnum = None):
        """Get all roles, optionally filtered by status"""
        query = Role.query
        if status:
            query = query.filter_by(status=status)
            logger.debug(f"Fetching roles with status {status}")
        else:
            logger.debug("Fetching all roles")
        return query.all()
    
    @staticmethod
    def update(role_id: int, **kwargs) -> Role | None:
        """
        Update role attributes
        
        Args:
            role_id: ID of role to update
            **kwargs: Fields to update:
                - name (str): Must be unique
                - rate (float): Hourly rate
                - status (RoleStatusEnum): ACTIVE/ARCHIVED
        """
        if not kwargs:
            logger.warning(f"Update aborted: No fields provided for role ID {role_id}")
            return None

        role = Role.query.get(role_id)
        if not role:
            logger.warning(f"Role ID {role_id} not found")
            return None

        if 'name' in kwargs and kwargs['name'] != role.name:
            if Role.query.filter_by(name=kwargs['name']).first():
                logger.warning(f"Role name '{kwargs['name']}' already exists")
                return None

        try:
            changes = False
            for key, value in kwargs.items():
                if hasattr(role, key) and value is not None:
                    old_value = getattr(role, key)
                    if old_value != value:
                        setattr(role, key, value)
                        logger.info(f"Updated {key} from '{old_value}' to '{value}'")
                        changes = True

            if not changes:
                logger.info(f"No changes for role ID {role_id}")
                return role

            db.session.commit()
            logger.info(f"Updated role ID {role_id}")
            return role
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Error updating role ID {role_id}: {str(e)}")
            raise

    @staticmethod
    def archive(role_id: int) -> bool:
        """Archive role if not assigned to employees"""
        role = Role.query.get(role_id)
        if not role:
            logger.warning(f"Role ID {role_id} not found")
            return False

        if role.employees:
            logger.warning(f"Cannot archive role ID {role_id} - "
                           f"Assigned to {len(role.employees)} employees")
            return False

        try:
            role.status = RoleStatusEnum.ARCHIVED
            role.archived_at = datetime.now(timezone.utc)
            db.session.commit()
            logger.info(f"Archived role ID {role_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Error archiving role ID {role_id}: {str(e)}")
            raise

    @staticmethod
    def restore(role_id: int) -> bool:
        """Restore an archived role"""
        role = Role.query.get(role_id)
        if not role:
            logger.warning(f"Role ID {role_id} not found")
            return False

        if role.status != RoleStatusEnum.ARCHIVED:
            logger.warning(f"Role ID {role_id} is not archived")
            return False

        try:
            role.status = RoleStatusEnum.ACTIVE
            role.archived_at = None
            db.session.commit()
            logger.info(f"Restored role ID {role_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Error restoring role ID {role_id}: {str(e)}")
            raise