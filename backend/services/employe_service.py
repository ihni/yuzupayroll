from backend.extensions import db
from backend.models import Employee, EmployeeStatusEnum
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError # type: ignore
from backend.utils import get_logger

logger = get_logger(__name__)

class EmployeeService:

    @staticmethod
    def create(first_name: str, last_name: str, email: str, role_id: int) -> Employee | None:
        """create a new employee 
        
        returns an employee object with an ACTIVE status if the no email was found to already exist,
        else it will return None
        """
        try:
            if Employee.query.filter_by(email=email).first():
                logger.warning(f"Email '{email}' already exists")
                return None

            employee = Employee(
                first_name=first_name,
                last_name=last_name,
                email=email,
                role_id=role_id,
                status=EmployeeStatusEnum.ACTIVE
            )
            
            db.session.add(employee)
            db.session.commit()
            logger.info(f"Created employee ID {employee.id}")
            return employee
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Error creating employee': {str(e)}")
            raise

    @staticmethod
    def get_by_id(emp_id: int) -> Employee | None:
        """get employee by ID"""
        employee = Employee.query.get(emp_id)
        if employee:
            logger.info(f"Found employee ID {emp_id}")
        else:
            logger.warning(f"Employee ID {emp_id} not found")
        return employee
    
    @staticmethod
    def get_all(status: EmployeeStatusEnum = None) -> list[Employee]:
        """get all employees, optionally filtered by status
        
        if status is given, it must be chosen from the EnumClass or else query will not return
        expected results
        """
        query = Employee.query
        if status:
            query = query.filter_by(status=status)
            logger.info(f"Fetching employees with status {status}")
        else:
            logger.info("Fetching all employees")
        return query.all()
    
    @staticmethod
    def update(emp_id: int, **kwargs) -> Employee | None:
        """
        update employee attributes
        
        args:
            emp_id: ID of the employee to update
            **kwargs: Attributes to update:
                - first_name (str)
                - last_name (str)
                - email (str): (must be unique)
                - role_id (int)
                - status (EmployeeStatusEnum): (ACTIVE/INACTIVE/ARCHIVED)
        """
               
        if not kwargs:
            logger.warning(f"Update aborted: No fields provided for employee ID {emp_id}")
            return None
        
        employee = Employee.query.get(emp_id)
        
        if not employee:
            logger.warning(f"Update failed: Employee ID {emp_id} not found")
            return None
        
        if employee.status == EmployeeStatusEnum.ARCHIVED:
            logger.warning(f"Update failed: Employee ID {emp_id} is archived")
            return None
        
        if 'email' in kwargs:
            new_email = kwargs['email']
            if new_email != employee.email and Employee.query.filter_by(email=new_email).first():
                logger.warning(f"Email '{new_email}' already in use")
                return None

        try:
            changes = False
            for key, value in kwargs.items():
                if hasattr(employee, key) and value is not None:
                    old_value = getattr(employee, key)
                    if old_value != value:
                        setattr(employee, key, value)
                        logger.info(f"Updating {key} from '{old_value}' to '{value}'")
                        changes = True

            if not changes:
                logger.info(f"No changes detected for employee ID {emp_id}")
                return employee
                
            db.session.commit()
            logger.info(f"Updated employee ID {emp_id}")
            return employee
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to update employee ID {emp_id}")
            raise

    @staticmethod
    def archive(emp_id: int) -> bool:
        """archive an employee"""
        employee = Employee.query.get(emp_id)
        if not employee:
            logger.warning(f"Archive failed: Employee ID {emp_id} not found")
            return False

        if employee.status == EmployeeStatusEnum.ARCHIVED:
            logger.warning(f"Employee ID {emp_id} already archived")
            return False

        try:
            employee.status = EmployeeStatusEnum.ARCHIVED
            employee.archived_at = datetime.now(timezone.utc)
            db.session.commit()
            logger.info(f"Archived employee ID {emp_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Error archiving employee ID {emp_id}")
            raise

    @staticmethod
    def restore(emp_id: int) -> bool:
        """restore an archived employee"""
        employee = Employee.query.get(emp_id)
        if not employee:
            logger.warning(f"Restore failed: Employee ID {emp_id} not found")
            return False

        if employee.status != EmployeeStatusEnum.ARCHIVED:
            logger.warning(f"Restore failed: Employee ID {emp_id} not archived")
            return False

        try:
            employee.status = EmployeeStatusEnum.ACTIVE
            employee.archived_at = None
            db.session.commit()
            logger.info(f"Restored employee ID {emp_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Error restoring employee ID {emp_id}")
            raise