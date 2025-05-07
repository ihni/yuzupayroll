from .. import db
from ..models import Employee

class EmployeeService:
    @staticmethod
    def create(employee: Employee):
        cnx = db.get_connection()
        cursor = cnx.cursor()

        query = """
            INSERT INTO employees (first_name, last_name, email, role_id)
            VALUES
            (%(first_name)s, %(last_name)s, %(email)s, %(role_id)s)
        """
        
        cursor.execute(query, employee.to_dict())
        cnx.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(emp_id: int) -> Employee:
        cnx = db.get_connection()
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from employees
            WHERE id = %s
        """

        cursor.execute(query, (emp_id,))
        row = cursor.fetchone()
        return Employee(**row) if row else None
    
    @staticmethod
    def update(emp_id: int, update_fields: dict) -> bool:
        # nothing to update
        if not update_fields:
            return False
        
        cnx = db.get_connection()
        cursor = cnx.cursor()

        # fields in the query and the values to set to
        set_clauses = []
        values = []

        for field, value in update_fields:
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
            return cursor.rowcount > 0
        except Exception as e:
            cnx.rollback()
            print(f"Udate error: {e}")
            return False
        
    @staticmethod
    def delete(emp_id: int) -> bool:
        cnx = db.get_connection()
        cursor = cnx.cursor()

        query = """
            DELETE FROM employees
            WHERE id = %s
        """

        try:
            cursor.execute(query, (emp_id,))
            cnx.commit()
            return cursor.rowcount > 0
        except Exception as e:
            pass
    
    @staticmethod
    def get_all():
        pass