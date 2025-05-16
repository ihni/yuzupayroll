from app.utils import get_logger
from app.extensions import db
from app.models import WorkLog

logger = get_logger(__name__)

class WorkLogService:

    @staticmethod
    def create(emp_id, date_worked, hours_worked):
        try:
            work_log = WorkLog(
                employee_id=emp_id,
                date_worked=date_worked,
                hours_worked=hours_worked
            )
            db.session.add(work_log)
            db.session.commit()
            logger.info(f"Created work log for employee {emp_id} on {date_worked}")
            return work_log
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Failed to create work log for employee id '{emp_id}'")
            raise
    
    @staticmethod
    def get_all():
        work_logs = WorkLog.query.all()
        logger.info(f"Fetched {len(work_logs)} work logs")
        return work_logs
    
    @staticmethod
    def get_by_id(work_log_id):
        work_log = WorkLog.query.get(work_log_id)
        if work_log:
            logger.info(f"Found work log id '{work_log_id}'")
        else:
            logger.info(f"No work log found with id '{work_log_id}'")
        return work_log
    
    @staticmethod
    def get_by_date_worked(date_worked):
        work_logs = WorkLog.query.filter_by(date_worked=date_worked).all()
        if work_logs:
            logger.info(f"Found '{len(work_logs)}' work logs on date '{date_worked}'")
        else: 
            logger.info(f"No work logs found on date '{date_worked}'")
        return work_logs
    
    @staticmethod
    def update(work_log_id, date_worked=None, hours_worked=None):
        work_log = WorkLog.query.get(work_log_id)
        if not work_log:
            logger.info(f"Update failed: No work log found with id '{work_log_id}'")
            return None

        if work_log.is_deleted:
            logger.info(f"Attempted update on work log id '{work_log_id}'")
            return None

        if not date_worked and not hours_worked:
            logger.info(f"Tried updating work log id '{work_log_id}' with empty fields")
            return None

        old_date = work_log.date_worked
        old_hours = work_log.hours_worked

        updates = {
            "date_worked": date_worked,
            "hours_worked": hours_worked,
        }

        for attr, value in updates:
            if value is not None:
                setattr(work_log, attr, value)

        try:
            db.session.commit()
            logger.info(f"Updated work log id '{work_log_id}'")
            if date_worked:
                logger.info(f"Date '{old_date} -> '{date_worked}'")
            if hours_worked:
                logger.info(f"Hours '{old_hours} -> '{hours_worked}'")
            return work_log
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error updating work log id '{work_log_id}'")
            raise

    @staticmethod
    def delete(work_log_id):
        work_log = WorkLog.query.get(work_log_id)
        if not work_log:
            logger.info(f"Delete failed: No work log found with id '{work_log_id}'")
            return False

        if work_log.is_deleted:
            logger.info(f"Delete failed: work log id '{work_log_id}' is already marked deleted")
            return False

        try:
            work_log.soft_delete()
            db.session.commit()
            logger.info(f"Deleted work log id '{work_log_id}'")
            return True
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error deleting work log id '{work_log_id}'")
            raise

    @staticmethod
    def restore(work_log_id):
        work_log = WorkLog.query.get(work_log_id)
        if not work_log:
            logger.info(f"Restore failed: No work log found with id '{work_log_id}'")
            return False
        
        if not work_log.is_deleted:
            logger.info(f"Restore failed: work log id '{work_log_id}' is not marked deleted")
            return False
            
        try:
            work_log.restore()
            db.session.commit()
            logger.info(f"Restored work log id '{work_log_id}'")
            return True
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error restoring work log id '{work_log_id}'")
            raise