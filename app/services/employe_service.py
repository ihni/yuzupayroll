from app.utils import get_logger
from app.extensions import db
from app.models import Employee

logger = get_logger(__name__)

class EmployeeService:

    @staticmethod
    def create(first_name, last_name, email, role_id):
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role_id=role_id
        )
        db.session.add(employee)
        db.session.commit()
        return employee
    
    @staticmethod
    def get_all():
        return Employee.query.all()

    @staticmethod
    def get_by_id(emp_id):
        return Employee.query.get(emp_id)