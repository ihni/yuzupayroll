from app.extensions import db
from app.models import PayrollWorklog, Worklog, WorklogStatusEnum
from sqlalchemy.exc import SQLAlchemyError # type: ignore
from app.utils import get_logger

logger = get_logger(__name__)

# TODO:
# ADD LOG STATEMENTS

class PayrollWorklogService:

    @staticmethod
    def bulk_create_associations(payroll_id: int, worklog_ids: list[int]) -> bool:
        """bulk create payroll-worklog associations"""
        try:
            worklogs = Worklog.query.filter_by(
                Worklog.id.in_(worklog_ids),
                Worklog.status == WorklogStatusEnum.ACTIVE).all()
            
            if (len(worklogs) != len(worklog_ids)):
                raise ValueError("Some work logs are invalid")

            associations = [
                PayrollWorklog(
                    payroll_id=payroll_id,
                    worklog_id=worklog.id,
                    hours_recorded=worklog.hours_worked
                ) for worklog in worklogs
            ]

            db.session.bulk_save_objects(associations)
            db.session.commit()
            logger.info("message")
            return True
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("message")
            return False

    @staticmethod
    def lock_snapshot(payroll_id: int) -> bool:
        """mark payroll as locked"""
        try:
            PayrollWorklog.query.filter_by(
                payroll_id=payroll_id
            ).update({'snapshot_locked': True})
            db.session.commit()
            logger.info("message")
            return True
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("message")
            return False