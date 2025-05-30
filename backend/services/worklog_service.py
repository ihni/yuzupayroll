from backend.extensions import db
from datetime import datetime, timezone
from backend.models import Worklog, WorklogStatusEnum
from sqlalchemy.exc import SQLAlchemyError # type: ignore
from backend.utils import get_logger

logger = get_logger(__name__)

class WorklogService:

    @staticmethod
    def create_worklog_shell(employee_id: int, date: datetime, hours_worked: float) -> Worklog:
        """create a work log shell from a valid employee id"""
        try:
            worklog = Worklog(
                employee_id=employee_id,
                date=date,
                hours_worked=hours_worked,
                status=WorklogStatusEnum.ACTIVE
            )
            db.session.add(worklog)
            db.session.commit()
            logger.info(f"Created work log for employee ID {employee_id} on {date}")
            return worklog
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to create work log for employee ID {employee_id}: {str(e)}")
            raise

    @staticmethod
    def get_eligible_for_payroll(employee_id: int, start: datetime, end: datetime) -> list[Worklog]:
        """fetches worklogs that fit the criteria and are active and not in a payroll"""
        from backend.models import Payroll, PayrollStatusEnum

        worklogs = Worklog.query.filter(
            Worklog.employee_id == employee_id,
            Worklog.date.between(start, end),
            Worklog.status != WorklogStatusEnum.ARCHIVED,
            ~Worklog.payroll_worklogs.any(Payroll.status == PayrollStatusEnum.DRAFT)
        ).all()

        logger.info(f"Fetched {len(worklogs)} eligible worklogs for employee ID {employee_id} between {start} - {end}")
        return worklogs
    
    @staticmethod
    def lock(worklog_id: int) -> bool:
        """lock a single work log"""
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
        """lock multiple worklogs in one transaction"""
        try:
            now = datetime.now(timezone.utc)
            updated_rows = (
                db.session.query(Worklog)
                .filter(Worklog.id.in_(worklog_ids))
                .update(
                    {
                        'status': WorklogStatusEnum.LOCKED,
                        'locked_at': now
                    },
                    synchronize_session='fetch'
                )
            )
            db.session.commit()
            logger.info(f"Bulk locked ({updated_rows}) work logs")
            return True
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception(f"Failed to bulk lock ({len(worklog_ids)}) work logs")
            return False
    
    @staticmethod
    def unlock(worklog_id: int) -> bool:
        worklog = Worklog.query.get(worklog_id)
        if not worklog:
            logger.warning(f"Unlock failed: Worklog ID {worklog_id} not found")
            return False
        
        from backend.services import PayrollWorklogService
        if PayrollWorklogService.is_worklog_in_finalized_payroll(worklog_id):
            logger.warning(f"Unlock failed: Worklog ID {worklog_id} is part of a locked payroll")
            return False
        
        if worklog.status != WorklogStatusEnum.LOCKED:
            logger.warning(f"Unlock failed: Worklog ID {worklog_id} is not locked")
            return False
        
        try:
            worklog.status = WorklogStatusEnum.ACTIVE
            worklog.locked_at = None
            db.session.commit()
            logger.info(f"Unlocked worklog ID {worklog_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to unlock worklog ID {worklog_id}: {str(e)}")
            raise

    @staticmethod
    def get_by_id(worklog_id: int) -> Worklog | None:
        """get work log by ID"""
        worklog = Worklog.query.get(worklog_id)
        if worklog:
            logger.info(f"Found work log ID {worklog_id}")
        else:
            logger.warning(f"Work log ID {worklog_id} not found")
        return worklog
    
    @staticmethod
    def get_all(status: WorklogStatusEnum = None) -> list[Worklog]:
        """get all work logs, optionally filtered by statu
        
        if status is given, it must be chosen from the EnumClass or else query will not return
        expected results
        """
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
        update work log attributes when in draft
        
        args:
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
    def archive(worklog_id: int) -> bool:
        worklog = Worklog.query.get(worklog_id)
        if not worklog:
            logger.warning(f"Worklog ID {worklog_id} not found")
            return False
        
        from backend.services.payroll_worklog_service import PayrollWorklogService
        if PayrollWorklogService.is_worklog_in_any_payroll(worklog_id):
            logger.warning(f"Cannot archive worklog ID {worklog_id} because it is in a payroll")
            return False
        if worklog.status == WorklogStatusEnum.LOCKED:
            logger.warning(f"Cannot archive locked worklog ID {worklog_id}")
            return False
        
        try:
            worklog.status = WorklogStatusEnum.ARCHIVED
            db.session.commit()
            logger.info(f"Archived worklog ID {worklog_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to archive worklog ID {worklog_id}")
            raise


    @staticmethod
    def restore(worklog_id: int) -> bool:
        worklog = Worklog.query.get(worklog_id)
        if not worklog:
            logger.warning(f"Restore failed: worklog ID {worklog_id} not found")
            return False

        if worklog.status != WorklogStatusEnum.ARCHIVED:
            logger.warning(f"Restore aborted: worklog ID {worklog_id} is not archived")
            return False

        try:
            worklog.status = WorklogStatusEnum.ACTIVE
            db.session.commit()
            logger.info(f"Restored worklog ID {worklog_id}")
            return True
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception(f"Failed to restore worklog ID {worklog_id}")
            return False