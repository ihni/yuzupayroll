from ..models import Payroll
from ..utils import get_logger, db_operation
import datetime

logger = get_logger(__name__)

class PayrollService:

    @staticmethod
    @db_operation(commit=True)
    def create(cursor, payroll: Payroll):
        query = """
            INSERT INTO payroll (pay_period_start, pay_period_end, gross_pay, total_hours, employee_id)
            VALUES
            (%(pay_period_start)s, %(pay_period_end)s, %(gross_pay)s, %(total_hours)s, %(employee_id)s)
        """
        cursor.execute(query, payroll.to_dict_for_insert())
        logger.info("Payroll created with ID: %s", cursor.lastrowid)
        return cursor.lastrowid

    @staticmethod
    @db_operation(fetch=True)
    def get_by_id(cursor, payroll_id: int) -> tuple:
        query = "SELECT * from payroll WHERE id = %s"
        return query, (payroll_id,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_date_range(cursor, start: datetime, end: datetime) -> tuple:
        query = """
            SELECT * from payroll
            WHERE pay_period_start BETWEEN %(pay_period_start)s AND %(pay_period_end)s
            AND pay_period_start BETWEEN %(pay_period_start)s AND %(pay_period_end)s
        """
        return query, (start, end,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_employee_id(cursor, emp_id: int) -> tuple:
        query = "SELECT * from payroll WHERE employee_id = %s"
        return query, (emp_id,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_total_hours(cursor, total_hours: int) -> tuple:
        query = "SELECT * from payroll WHERE total_hours = %s"
        return query, (total_hours,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_gross_pay(cursor, gross_pay: int) -> tuple:  
        query = "SELECT * from payroll WHERE gross_pay = %s"
        return query, (gross_pay,)

    @staticmethod
    @db_operation(commit=True)
    def update(cursor, payroll_id: int, update_fields: dict) -> bool:
        if not update_fields:
            logger.warning("Empty update fields were passed.")
            return False

        set_clauses = []
        values = []

        for field, value in update_fields.items():
            set_clauses.append(f"{field} = %s")
            values.append(value)
        values.append(payroll_id)

        query = f"""
            UPDATE payroll SET {', '.join(set_clauses)}
            WHERE id = %s
        """

        cursor.execute(query, values)
        return cursor.rowcount > 0

    @staticmethod
    @db_operation(commit=True)
    def delete(cursor, payroll_id: int) -> bool:
        query = "DELETE FROM payroll WHERE id = %s"
        cursor.execute(query, (payroll_id,))
        return cursor.rowcount > 0
    
    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_all(cursor) -> tuple:
        query = "SELECT * FROM payroll"
        return query, ()