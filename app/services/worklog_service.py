from app.extensions import db
from datetime import datetime, timezone
from app.models import Worklog, WorklogStatusEnum
from sqlalchemy.exc import SQLAlchemyError
from app.utils import get_logger

logger = get_logger(__name__)

class WorklogService:

    @staticmethod
    def create_worklog_shell(emp_id: int, date: datetime, hours_worked: float):
        """Creates a work log shell from a valid employee id"""
        try:
            worklog = Worklog(employee_id=emp_id,
                              date=date,
                              hours_worked=hours_worked,
                              status=WorklogStatusEnum.ACTIVE)
            db.session.add(worklog)
            db.session.commit()
            logger.info(f"Created work log for employee ID {emp_id} on {date}")
            return worklog
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to create work log for employee ID {emp_id}: {str(e)}")
            raise

    @staticmethod
    def get_eligible_for_payroll(emp_id: int, start: datetime, end: datetime) -> list[dict]:
        """Returns serialized worklog data for payroll processing"""
        worklogs = Worklog.query.filter_by(Worklog.employee_id == emp_id,
                                           Worklog.date.between(start, end),
                                           Worklog.status == WorklogStatusEnum.ACTIVE).all()
        logger.info(f"Serialized ({len(worklogs)}) work logs for employee ID {emp_id} between {start} - {end}")
        return [{'id': w.id,
                 'hours_worked': w.hours_worked,
                 'date': w.date} 
                 for w in worklogs]

    @staticmethod
    def lock(worklog_id: int) -> bool:
        """Locks a single work log"""
        worklog = Worklog.query.get(worklog_id)
        if not worklog:
            logger.warning(f"Work log ID {worklog_id} not found")
            return False

        try:
            worklog.status = WorklogStatusEnum.LOCKED
            worklog.locked_at = datetime.now(timezone.utc)
            db.session.commit()
            logger.info(f"Locked work log ID {worklog_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to lock work log ID {worklog_id}")
            raise
        
    @staticmethod
    def bulk_lock(worklog_ids: list[int]) -> bool:
        """Locks multiple worklogs in one transaction"""
        try:
            # use model instead of db session
            db.session.query(Worklog).filter(
                Worklog.id.in_(worklog_ids)
            ).update({
                'status': WorklogStatusEnum.LOCKED,
                'locked_at': datetime.utcnow()
            })
            db.session.commit()
            logger.info(f"Bulk locked ({len(worklog_ids)}) work logs")
            return True
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception(f"Failed to bulk lock ({len(worklog_ids)}) work logs")
            return False
    
    # TODO:
    # ONLY UNLOCK WHEN NOT IN PAYROLL
    @staticmethod
    def unlock(worklog_id: int) -> bool:
        pass

    @staticmethod
    def get_by_id(worklog_id) -> Worklog | None:
        """Get work log by ID"""
        worklog = Worklog.query.get(worklog_id)
        if worklog:
            logger.info(f"Found work log ID {worklog_id}")
        else:
            logger.warning(f"Work log ID {worklog_id} not found")
        return worklog
    
    @staticmethod
    def get_all(status: WorklogStatusEnum = None) -> list[Worklog]:
        """Get all work logs, optionally filtered by status"""
        query = Worklog.query
        if status:
            query = query.filter_by(status=status)
            logger.info(f"Fetching work logs with status {status}")
        else:
            logger.info("Fetching all work logs")
        return query.all()
    
    @staticmethod
    def get_by_date(date: datetime) -> list[Worklog]:
        worklogs = Worklog.query.filter_by(date=date).all()
        if worklogs:
            logger.info(f"Found ({len(worklogs)}) work logs on date '{date}'")
        else: 
            logger.info(f"No work logs found on date '{date}'")
        return worklogs
    

    @staticmethod
    def update(worklog_id: int, **kwargs) -> Worklog | None:
        """
        Update work log attributes ONLY WHEN STATUS IS IN DRAFT
        
        Args:
            worklog_id: ID of the work log to update
            **kwargs: Attributes to update:
                - date (datetime)
                - hours_worked (float)
        """
               
        if not kwargs:
            logger.warning(f"Update aborted: No fields provided for work log ID {worklog_id}")
            return None
        
        worklog = Worklog.query.get(worklog_id)
        
        if not worklog:
            logger.warning(f"Update failed: Work log ID {worklog_id} not found")
            return None
        
        if worklog.status != WorklogStatusEnum.ACTIVE:
            logger.warning(f"Update failed: Work log ID {worklog_id} is either locked or archived")
            return None

        try:
            changes = False
            for key, value in kwargs.items():
                if hasattr(worklog, key) and value is not None:
                    old_value = getattr(worklog, key)
                    if old_value != value:
                        setattr(worklog, key, value)
                        logger.info(f"Updating {key} from '{old_value}' to '{value}'")
                        changes = True

            if not changes:
                logger.info(f"No changes detected for work log ID {worklog_id}")
                return worklog
                
            db.session.commit()
            logger.info(f"Updated work log ID {worklog_id}")
            return worklog
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to update work log ID {worklog_id}")
            raise
    
    @staticmethod
    # TODO:
    # ONLY ARCHIVE IF WORKLOG IS NOT LOCKED AND IS NOT IN PAYROLL
    # OR IF LOGGED IN THE PAYROLL_WORKLOGS TABLE
    def archive(worklog_id):
        pass

    @staticmethod
    def restore(work_log_id):
        pass