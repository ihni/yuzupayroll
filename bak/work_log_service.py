from ..models import WorkLog
from ..utils import get_logger, db_operation
import datetime

logger = get_logger(__name__)

class WorkLogService:
    @staticmethod
    @db_operation(commit=True)
    def create(cursor, work_log: WorkLog):
        query = """
            INSERT INTO work_logs (date_worked, hours_worked, employee_id)
            VALUES (%(date_worked)s, %(hours_worked)s, %(employee_id)s)
        """
        cursor.execute(query, work_log.to_dict_for_insert())
        logger.info("Work log created with ID: %s", cursor.lastrowid)
        return cursor.lastrowid

    @staticmethod
    @db_operation(fetch=True)
    def get_by_id(cursor, work_log_id: int) -> tuple:
        query = "SELECT * from work_logs WHERE id = %s"
        return query, (work_log_id,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_date(cursor, date: datetime) -> tuple:
        query = "SELECT * from work_logs WHERE date_worked = %s"
        return query, (date,)
    
    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_employee_id(cursor, emp_id: int) -> tuple:
        query = "SELECT * from work_logs WHERE employee_id = %s"
        return query, (emp_id,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_hour_worked(cursor, hours_worked: int) -> tuple:    
        query = "SELECT * from work_logs WHERE hours_worked = %s"
        return query, (hours_worked,)

    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_by_date_range(cursor, 
                         start_date: datetime.date, 
                         end_date: datetime.date) -> tuple:
        query = """
            SELECT * FROM work_logs 
            WHERE date_worked BETWEEN %s AND %s
            ORDER BY date_worked
        """, 
        return query, (start_date, end_date,)
    
    @staticmethod
    @db_operation(commit=True)
    def update(cursor, work_log_id: int, update_fields: dict) -> bool:
        if not update_fields:
            logger.warning("Empty update fields were passed.")
            return False

        set_clauses = []
        values = []

        for field, value in update_fields.items():
            set_clauses.append(f"{field} = %s")
            values.append(value)
        values.append(work_log_id)

        query = f"""
            UPDATE work_logs SET {', '.join(set_clauses)}
            WHERE id = %s
        """

        cursor.execute(query, values)
        return cursor.rowcount > 0
        
    @staticmethod
    @db_operation(commit=True)
    def delete(cursor, work_log_id: int) -> bool:
        query = "DELETE FROM work_logs WHERE id = %s"
        cursor.execute(query, (work_log_id,))
        return cursor.rowcount > 0
      
    @staticmethod
    @db_operation(fetch=True, fetch_many=True)
    def get_all(cursor) -> tuple:
        query = "SELECT * FROM work_logs"
        return query, ()