from app.utils import get_logger
from app.extensions import db
from app.models import Employee
from datetime import datetime, timezone

logger = get_logger(__name__)

class EmployeeService:

    @staticmethod
    def create(first_name, last_name, email, role_id, status='ACTIVE'):
        try:
            employee = Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                role_id=role_id,
                status=status
            )
            db.session.add(employee)
            db.session.commit()
            logger.info(f"Created employee with id '{employee.id}'")
            return employee
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error creating employee': {e}")
            raise

    @staticmethod
    def get_all():
        employees = Employee.query.all()
        logger.info(f"Fetched {len(employees)} employee/s")
        return employees
    
    @staticmethod
    def get_all_active():
        employees = Employee.query.filter_by(is_archived=False).all()
        logger.info(f"Fetched {len(employees)} active employee/s")
        return employees

    @staticmethod
    def get_all_archived():
        employees = Employee.query.filter_by(is_archived=True).all()
        logger.info(f"Fetched {len(employees)} deleted employee/s")
        return employees

    @staticmethod
    def get_by_id(emp_id):
        employee = Employee.query.get(emp_id)
        if employee:
            logger.info(f"Found employee id '{emp_id}'")
        else:
            logger.info(f"No employee found with id '{emp_id}'")
        return employee
    
    @staticmethod
    def update(emp_id, 
               first_name=None, 
               last_name=None, 
               email=None, 
               role_id=None,
               status=None):
        
        employee = Employee.query.get(emp_id)
        if not employee:
            logger.info(f"Update failed: No employee found with id '{emp_id}'")
            return None
        
        if employee.is_archived:
            logger.info(f"Attempted update on archived employee id '{emp_id}'")
            return None
        
        if not any([first_name, last_name, email, role_id, status]):
            logger.info(f"Tried updating employee id '{employee.role_id}' with no fields provided")
            return None

        if email and email != employee.email:
            existing = Employee.query.filter_by(email=email).first()
            if existing:
                logger.info(f"Update failed: Email '{email}' already in use")
                return None

        old_first_name = employee.first_name
        old_last_name = employee.last_name
        old_email = employee.email
        old_role = employee.role.name
        old_status = employee.status

        updates = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role_id": role_id,
            "status": status,
        }

        for attr, value in updates.items():
            if value is not None:
                setattr(employee, attr, value)

        try:
            db.session.commit()
            logger.info(f"Updated employee id '{emp_id}'")
            if first_name:
                logger.info(f"First name '{old_first_name} -> '{first_name}'")
            if last_name:
                logger.info(f"Last name '{old_last_name} -> '{last_name}'")
            if email:
                logger.info(f"Email '{old_email} -> '{email}'")
            if role_id:
                logger.info(f"Role '{old_role} -> '{employee.role.name}'")
            if status:
                logger.info(f"Status '{old_status}' -> '{status}'")
            return employee
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error updating employee id '{emp_id }'")
            raise

    @staticmethod
    def archive(emp_id):
        employee = Employee.query.get(emp_id)
        if not employee:
            logger.info(f"Archive failed: No employee found with id '{emp_id}'")
            return False
        
        if employee.is_archived:
            logger.info(f"Archive failed: employee id '{emp_id}' is already marked archived")
            return False
            
        try:
            employee.is_archived = True # do i change status as well?
            employee.archived_at = datetime.now(timezone.utc)
            db.session.commit()
            logger.info(f"Archived employee id '{emp_id}'")
            return True
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error archiving employee id '{emp_id}'")
            raise

    @staticmethod
    def restore(emp_id):
        employee = Employee.query.get(emp_id)
        if not employee:
            logger.info(f"Restore failed: No employee found with id '{emp_id}'")
            return False
        
        if not employee.is_archived:
            logger.info(f"Restore failed: employee id '{emp_id}' is not marked deleted")
            return False
            
        try:
            employee.is_archived = False
            employee.archived_at = None
            db.session.commit()
            logger.info(f"Restored employee id '{emp_id}'")
            return True
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error restoring employee id '{emp_id}'")
            raise