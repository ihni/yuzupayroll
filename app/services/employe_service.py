from app.utils import get_logger
from app.extensions import db
from app.models import Employee
from datetime import datetime, timezone

logger = get_logger(__name__)

class EmployeeService:

    @staticmethod
    def create(first_name, last_name, email, role_id):
        try:
            employee = Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                role_id=role_id
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
        logger.info(f"Fetched {len(employees)} roles")
        return employees

    @staticmethod
    def get_by_id(emp_id):
        employee = Employee.query.get(emp_id)
        if employee:
            logger.info(f"Found employee id '{emp_id}'")
        else:
            logger.info(f"No employee found with id '{emp_id}'")
        return Employee.query.get(emp_id)
    
    @staticmethod
    def update(emp_id, first_name=None, last_name=None, email=None, role_id=None):
        employee = Employee.query.get(emp_id)
        if not employee:
            logger.info(f"Update failed: No employee found with id '{emp_id}'")
            return None
        
        if not any([first_name, last_name, email, role_id]):
            logger.info("Tried updating employee id '{employee.role_id}' with empty fields")
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

        updates = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role_id": role_id,
        }

        for attr, value in updates:
            if value is not None:
                setattr(employee, attr, value)

        try:
            db.session.commit()
            logger.info(f"Updated employee id {emp_id}")
            if first_name:
                logger.info(f"First name '{old_first_name} -> '{first_name}'")
            if last_name:
                logger.info(f"Last name '{old_last_name} -> '{last_name}'")
            if email:
                logger.info(f"Email '{old_email} -> '{email}'")
            if role_id:
                logger.info(f"Role '{old_role} -> '{employee.role.name}'")
            return employee
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error updating employee id '{emp_id }'")
            raise

    @staticmethod
    def delete(emp_id):
        employee = Employee.query.get(emp_id)
        if not employee:
            logger.info(f"Delete failed: No employee found with id '{emp_id}'")
            return False
        
        if employee.is_deleted:
            logger.info(f"Delete failed: employee id '{emp_id}' is already marked deleted")
            return False
            
        try:
            employee.is_deleted = True
            employee.deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            logger.info(f"Soft deleted employee id '{emp_id}'")
            return True
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error deleting employee id '{emp_id}'")
            raise

    #TODO:
    # add a restore function later