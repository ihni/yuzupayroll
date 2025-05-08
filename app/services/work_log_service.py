from .. import db
from mysql.connector import Error as MySQLError
from ..models import WorkLog
from ..utils import get_logger
import datetime

logger = get_logger(__name__)

class WorkLogService:
    @staticmethod
    def create(work_log: WorkLog):
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor()

        query = """
            INSERT INTO work_logs (date_worked, hours_worked, employee_id)
            VALUES
            (%(date_worked)s, %(hours_worked)s, %(employee_id)s)
        """

        try:
            cursor.execute(query, work_log.to_dict_for_insert())
            cnx.commit()
            logger.info("Work log created with ID: %s", cursor.lastrowid)
            return cursor.lastrowid
        except MySQLError as err:
            cnx.rollback()
            logger.error("Failed to create work log: %s", err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_id(work_log_id: int) -> WorkLog:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return None
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from work_logs
            WHERE id = %s
        """

        try:
            cursor.execute(query, (work_log_id,))
            row = cursor.fetchone()
            logger.info("Fetched work log id (%s), returning results.", work_log_id)
            return WorkLog(**row) if row else None
        except MySQLError as err:
            logger.error("Failed to fetch work log id (%s): %s", work_log_id, err)
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_by_date(date: datetime) -> list[WorkLog]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from work_logs
            WHERE date_worked = %s
        """

        try:
            cursor.execute(query, (date,))
            rows = cursor.fetchall()
            logger.info("Fetched all work logs with date (%s), returning results.", date)
            return [WorkLog(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch work logs with date (%s): %s", date, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_employee_id(emp_id: int) -> list[WorkLog]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from work_logs
            WHERE employee_id = %s
        """

        try:
            cursor.execute(query, (emp_id,))
            rows = cursor.fetchall()
            logger.info("Fetched all work logs with employee id (%s), returning results.", emp_id)
            return [WorkLog(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch work logs with employee id (%s): %s", emp_id, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_by_hour_worked(hours_worked: int) -> list[WorkLog]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)
        
        query = """
            SELECT * from work_logs
            WHERE hours_worked = %s
        """

        try:
            cursor.execute(query, (hours_worked,))
            rows = cursor.fetchall()
            logger.info("Fetched all work logs with hour/s amount (%s), returning results.", hours_worked)
            return [WorkLog(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch work logs with hour/s amount (%s): %s", hours_worked, err)
            return []
        finally:
            cursor.close()

    @staticmethod
    def update(work_log_id: int, update_fields: dict) -> bool:
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
        values.append(work_log_id)

        query = f"""
            UPDATE work_logs
            SET {', '.join(set_clauses)}
            WHERE id = %s
        """

        try:
            cursor.execute(query, values)
            cnx.commit()
            logger.info("Executed update on work log id (%s), returning results", work_log_id)
            return cursor.rowcount > 0
        except MySQLError as err:
            cnx.rollback()
            logger.error("Failed to update work log id (%s): %s", work_log_id, err)
            return False
        finally:
            cursor.close()
        
    @staticmethod
    def delete(work_log_id: int) -> bool:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return False
        cursor = cnx.cursor()

        query = """
            DELETE FROM work_logs
            WHERE id = %s
        """

        try:
            cursor.execute(query, (work_log_id,))
            cnx.commit()
            logger.info("Executed deletion on work log id (%s), returning results", work_log_id)
            return cursor.rowcount > 0
        except MySQLError as err:
            logger.error("Failed to delete work log id (%s): %s", work_log_id, err)
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_all() -> list[WorkLog]:
        cnx = db.get_connection()
        if not cnx:
            logger.error("No database connection available.")
            return []
        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT * FROM work_logs
        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            logger.info("Fetched all work logs, returning results.")
            return [WorkLog(**row) for row in rows] if rows else []
        except MySQLError as err:
            logger.error("Failed to fetch all work logs: %s", err)
            return []
        finally:
            cursor.close()