from backend.extensions import db
from backend.models import PayrollWorklog, Worklog, Payroll, PayrollStatusEnum, WorklogStatusEnum
from sqlalchemy.exc import SQLAlchemyError  # type: ignore
from sqlalchemy.orm import joinedload       # type: ignore
from backend.utils import get_logger

logger = get_logger(__name__)

# TODO:
# ADD LOG STATEMENTS

class PayrollWorklogService:

    @staticmethod
    def get_worklogs_for_payroll(payroll_id: int) -> list[PayrollWorklog]:
        """fetches all worklogs added to payroll"""
        payroll_worklogs = (
            PayrollWorklog.query
            .options(joinedload(PayrollWorklog.worklog))  # eager load the worklog relationship
            .filter_by(payroll_id=payroll_id)
            .all()
        )
        return payroll_worklogs

    @staticmethod
    def is_worklog_in_finalized_payroll(worklog_id: int) -> bool:
        """returns true if the worklog is part of any non draft payroll"""
        return PayrollWorklog.query.join(Payroll).filter(
            PayrollWorklog.worklog_id == worklog_id,
            Payroll.status == PayrollStatusEnum.FINALIZED
        ).count() > 0
    
    @staticmethod
    def is_worklog_in_any_payroll(worklog_id: int) -> bool:
        """returns true if the worklog is part of any payroll"""
        return PayrollWorklog.query.join(Payroll).filter(
            PayrollWorklog.worklog_id == worklog_id,
            Payroll.status == PayrollStatusEnum.FINALIZED
        ).count() > 0

    @staticmethod
    def bulk_create_associations(payroll_id: int, worklog_ids: list[int]) -> bool:
        """bulk create payroll-worklog associations"""
        try:
            worklogs = Worklog.query.filter(
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
            PayrollWorklog.query.filter_by(payroll_id=payroll_id).update(
                {'snapshot_locked': True}, synchronize_session='fetch'
            )
            db.session.commit()
            logger.info(f"Snapshot locked payroll worklogs for payroll ID {payroll_id}")
            return True
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception(f"Failed to lock snapshot payroll worklogs for payroll ID {payroll_id}")
            return False

    @staticmethod
    def create_association(payroll_id: int, worklog_id: int) -> bool:
        """Attach exactly one worklog to a payroll."""
        try:
            pw = PayrollWorklog(
                payroll_id=payroll_id,
                worklog_id=worklog_id,
                hours_recorded=Worklog.query.get(worklog_id).hours_worked
            )
            db.session.add(pw)
            db.session.commit()
            logger.info(f"Associated worklog {worklog_id} to payroll {payroll_id}")
            return True
        except SQLAlchemyError:
            db.session.rollback()
            logger.exception(f"Failed to associate worklog {worklog_id}")
            return False

    @staticmethod
    def remove_association(payroll_id: int, worklog_id: int) -> bool:
        """
        remove the link between a payroll and a worklog - only allowed if the payroll 
        is still in DRAFT.
        """
        payroll = Payroll.query.get(payroll_id)
        if not payroll or payroll.status != PayrollStatusEnum.DRAFT:
            logger.warning(f"Cannot remove worklog: payroll {payroll_id} is not in DRAFT status")
            return False

        try:
            deleted = PayrollWorklog.query.filter_by(
                payroll_id=payroll_id,
                worklog_id=worklog_id
            ).delete()
            if not deleted:
                logger.warning(f"No association found for payroll {payroll_id} & worklog {worklog_id}")
                return False

            db.session.commit()
            logger.info(f"Removed worklog {worklog_id} from payroll {payroll_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to remove worklog {worklog_id} from payroll {payroll_id}: {e}")
            return False