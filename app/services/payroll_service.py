from .. import db
from mysql.connector import Error as MySQLError
from ..models import Payroll
from ..utils import get_logger
import datetime

logger = get_logger(__name__)

class PayrollService:
    @staticmethod
    def create(payroll: Payroll):
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor()

        query = """
            INSERT INTO payroll (pay_period_start, pay_period_end, gross_pay, total_hours, employee_id)
            VALUES
            (%(pay_period_start)s, %(pay_period_end)s, %(gross_pay)s, %(total_hours)s, %(employee_id)s)
        """

        try:
            cursor.execute(query, payroll.to_dict())
            cnx.commit()
            logger.info("Payroll created with ID: %s", cursor.lastrowid)
            return cursor.lastrowid
        except MySQLError as err:
            cnx.rollback()
            logger.error("Failed to create payroll: %s", err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(payroll_id: int) -> Payroll:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from payroll
            WHERE id = %s
        """

        try:
            cursor.execute(query, (payroll_id,))
            row = cursor.fetchone()
            logger.info("Fetched payroll id (%s), returning results.", payroll_id)
            return Payroll(**row) if row else None
        except MySQLError as err:
            logger.error("Failed to fetch payroll id (%s): %s", payroll_id, err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_date_range(start: datetime, end: datetime) -> list[Payroll]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from payroll
            WHERE date BETWEEN %(pay_period_start)s AND %(pay_period_end)s
        """

        try:
            cursor.execute(query, (start, end,))
            rows = cursor.fetchall()
            logger.info("Fetched all payrolls with date range between (%s - %s), returning results.", start, end)
            return [Payroll(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch payrolls with date range between (%s - %s): %s", start, end, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_employee_id(emp_id: int) -> list[Payroll]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from payroll
            WHERE employee_id = %s
        """

        try:
            cursor.execute(query, (emp_id,))
            rows = cursor.fetchall()
            logger.info("Fetched all payrolls with employee id (%s), returning results.", emp_id)
            return [Payroll(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch payrolls with employee id (%s): %s", emp_id, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_total_hours(total_hours: int) -> list[Payroll]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from payroll
            WHERE total_hours = %s
        """

        try:
            cursor.execute(query, (total_hours,))
            rows = cursor.fetchall()
            logger.info("Fetched all payrolls with total hours (%s), returning results.", total_hours)
            return [Payroll(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch payrolls with total hours (%s): %s", total_hours, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_gross_pay(gross_pay: int) -> list[Payroll]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from payroll
            WHERE gross_pay = %s
        """

        try:
            cursor.execute(query, (gross_pay,))
            rows = cursor.fetchall()
            logger.info("Fetched all payrolls with gross pay (%s), returning results.", gross_pay)
            return [Payroll(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch payrolls with gross pay (%s): %s", gross_pay, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def update(payroll_id: int, update_fields: dict) -> bool:
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

        for field, value in update_fields.items():
            set_clauses.append(f"{field} = %s")
            values.append(value)

        # where clause
        values.append(payroll_id)

        query = f"""
            UPDATE payroll
            SET {', '.join(set_clauses)}
            WHERE id = %s
        """

        try:
            cursor.execute(query, values)
            cnx.commit()
            logger.info("Executed update on payroll id (%s), returning results", payroll_id)
            return cursor.rowcount > 0
        except MySQLError as err:
            cnx.rollback()
            logger.error("Failed to update payroll id (%s): %s", payroll_id, err)
            return False
        finally:
            cursor.close()
        
    @staticmethod
    def delete(payroll_id: int) -> bool:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return False
        cursor = cnx.cursor()

        query = """
            DELETE FROM payroll
            WHERE id = %s
        """

        try:
            cursor.execute(query, (payroll_id,))
            cnx.commit()
            logger.info("Executed deletion on payroll id (%s), returning results", payroll_id)
            return cursor.rowcount > 0
        except MySQLError as err:
            logger.error("Failed to delete payroll id (%s): %s", payroll_id, err)
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_all() -> list[Payroll]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT * FROM payroll
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            logger.info("Fetched all payrolls, returning results.")
            return [Payroll(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch all payrolls: %s", err)
            return []
        finally:
            cursor.close()