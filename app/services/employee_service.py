from ..models import Employee
from ..utils import (
    get_logger, 
    db_operation,
)
logger = get_logger(__name__)

class EmployeeService:

    @staticmethod
    @db_operation(commit=True)
    def create(cursor, employee: Employee):
        query = """
            INSERT INTO employees (first_name, last_name, email, role_id)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(role_id)s)
        """
        cursor.execute(query, employee.to_dict_for_insert())
        logger.info("Employee created with ID: %s", cursor.lastrowid)
        return {"id": cursor.lastrowid}

    @staticmethod
    @db_operation(fetch=True)
    def get_by_id(cursor, emp_id: int) -> tuple:
        query = "SELECT * from employees WHERE id = %s"
        return query, (emp_id,)

    @staticmethod
    @db_operation(fetch=True)
    def get_by_email(cursor, emp_email: str) -> tuple:
        query = "SELECT * from employees WHERE email = %s"
        return query, (emp_email,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_role_id(cursor, role_id: int) -> tuple:
        query = "SELECT * from employees WHERE role_id = %s"
        return query, (role_id,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_role_name(cursor, role_name: str) -> tuple:
        like_pattern = f"%{role_name}%"
        query = """
            SELECT * FROM employees
            INNER JOIN roles ON employees.role_id IN (
                SELECT id FROM roles WHERE role.name LIKE %s
            )
        """
        return query, (like_pattern,)

    @staticmethod
    @db_operation(commit=True)
    def update(cursor, emp_id: int, update_fields: dict) -> bool:
        if not update_fields:
            logger.warning("Empty update fields were passed.")
            return False
        
        set_clauses = []
        values = []

        for field, value in update_fields.items():
            set_clauses.append(f"{field} = %s")
            values.append(value)
        values.append(emp_id) # where clause

        query = f"""
            UPDATE employees SET {', '.join(set_clauses)}
            WHERE id = %s
        """
        cursor.execute(query, values)
        return cursor.rowcount > 0
    
    @staticmethod
    @db_operation(commit=True)
    def delete(cursor, emp_id: int) -> bool:
        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
        return cursor.rowcount > 0
    
    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_all(cursor) -> tuple:
        query = "SELECT * FROM employees"
        return query, ()