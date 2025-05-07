from .. import db
from mysql.connector import Error as MySQLError
from ..models import Employee
from ..utils import get_logger

logger = get_logger(__name__)

class EmployeeService:
    @staticmethod
    def create(employee: Employee):
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor()

        query = """
            INSERT INTO employees (first_name, last_name, email, role_id)
            VALUES
            (%(first_name)s, %(last_name)s, %(email)s, %(role_id)s)
        """

        try:
            cursor.execute(query, employee.to_dict())
            cnx.commit()
            logger.info("Employee created with ID: %s", cursor.lastrowid)
            return cursor.lastrowid
        except MySQLError as err:
            cnx.rollback()
            logger.error("Failed to create Employee: %s", err)
            return None
        finally:
            cursor.close()     

    @staticmethod
    def get_by_id(emp_id: int) -> Employee:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from employees
            WHERE id = %s
        """

        try:
            cursor.execute(query, (emp_id,))
            row = cursor.fetchone()
            logger.info("Fetched employee id (%s), returning results.", emp_id)
            return Employee(**row) if row else None
        except MySQLError as err:
            logger.error("Failed to fetch employee id (%s): %s", emp_id, err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_email(emp_email: str) -> Employee:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from employees
            WHERE email = %s
        """

        try:
            cursor.execute(query, (emp_email,))
            row = cursor.fetchone()
            logger.info("Fetched employee email (%s), returning results.", emp_email)
            return Employee(**row) if row else None
        except MySQLError as err:
            logger.error("Failed to fetch employee email (%s): %s", emp_email, err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_role_id(role_id: int) -> list[Employee]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from employees
            WHERE role_id = %s
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            logger.info("Fetched all employees with role (%s), returning results.", role_id)
            return [Employee(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch employees with role (%s): %s", role_id, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def update(emp_id: int, update_fields: dict) -> bool:
        # nothing to update
        if not update_fields:
            logger.warning("Empty update fields were passed.")
            return False
        
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return False
        cursor = cnx.cursor()

        # fields in the query and the values to set to
        set_clauses = []
        values = []

        for field, value in update_fields.items:
            set_clauses.append(f"{field} = %s")
            values.append(value)

        # where clause
        values.append(emp_id)

        query = f"""
            UPDATE employees
            SET {', '.join(set_clauses)}
            WHERE id = %s
        """

        try:
            cursor.execute(query, values)
            cnx.commit()
            logger.info("Executed update on employee id (%s), returning results", emp_id)
            return cursor.rowcount > 0
        except MySQLError as err:
            cnx.rollback()
            logger.error("Failed to update employee id (%s): %s", emp_id, err)
            return False
        finally:
            cursor.close()
        
    @staticmethod
    def delete(emp_id: int) -> bool:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return False
        cursor = cnx.cursor()

        query = """
            DELETE FROM employees
            WHERE id = %s
        """

        try:
            cursor.execute(query, (emp_id,))
            cnx.commit()
            logger.info("Executed deletion on employee id (%s), returning results", emp_id)
            return cursor.rowcount > 0
        except MySQLError as err:
            logger.error("Failed to delete employee id (%s): %s", emp_id, err)
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_all() -> list[Employee]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT * FROM employees
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            logger.info("Fetched all employees, returning results.")
            return [Employee(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch all employees: %s", err)
            return []
        finally:
            cursor.close()