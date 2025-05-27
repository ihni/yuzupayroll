from app.extensions import db
from app.models import Payroll, PayrollStatusEnum
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError # type: ignore
from app.utils import get_logger

logger = get_logger(__name__)

class PayrollService:

    @staticmethod
    def create_payroll(employee_id: int, start_date: datetime, end_date: datetime) -> Payroll:
        """create a payroll shell from a valid employee id"""
        try:
            payroll = Payroll(
                employee_id=employee_id,
                start_date=start_date,
                end_date=end_date,
                gross_pay=0.00,
                net_pay=0.00,
                status=PayrollStatusEnum.DRAFT
            )
            db.session.add(payroll)
            db.session.flush()
            logger.info(f"Created payroll ID {payroll.id}")
            return payroll
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Payroll creation failed: {str(e)}")
            raise

    @staticmethod
    def calculate_totals(payroll_id: int) -> Payroll:
        """calculate payroll totals from provided worklogs data
        
        data being calculated are the total hours, gross pay, and net pay
        """
        payroll = Payroll.query.get(payroll_id)
        if not payroll:
            raise ValueError("Payroll not found")

        # Sum hours_recorded from payroll_worklogs linked to this payroll
        total_hours = sum(pw.hours_recorded for pw in payroll.payroll_worklogs)

        try:
            payroll.gross_pay = total_hours * payroll.employee.role.rate
            payroll.net_pay = payroll.gross_pay * (1 - payroll.organization.tax_rate)
            db.session.commit()
            logger.info(f"Calculated totals for payroll ID {payroll_id}: hours={total_hours}, gross={payroll.gross_pay}, net={payroll.net_pay}")
            return payroll
            return payroll
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Payroll calculation failed: {str(e)}")
            raise

    @staticmethod
    def finalize(payroll_id: int) -> bool:
        """finalize a payroll - only if all linked worklogs are locked"""
        payroll = Payroll.query.get(payroll_id)
        if not payroll:
            return False

        if any(pw.worklog.status != 'LOCKED' for pw in payroll.payroll_worklogs):
            logger.warning(f"Cannot finalize payroll ID {payroll_id} because some worklogs are not locked")
            return False

        try:
            payroll.status = PayrollStatusEnum.FINALIZED
            payroll.finalized_at = datetime.now(timezone.utc)

            
            from app.services import PayrollWorklogService 
            success = PayrollWorklogService.lock_snapshot(payroll_id)

            if not success:
                logger.error(f"Failed to lock snapshot payroll_worklogs for payroll ID {payroll_id}")
                db.session.rollback()
                return False

            db.session.commit()
            logger.info(f"Finalized payroll ID {payroll_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to finalize payroll ID {payroll_id}: {str(e)}")
            raise
    
    @staticmethod
    def get_all(status: PayrollStatusEnum = None) -> list[Payroll]:
        """get all payrolls, optionally filtered by status
        
        if status is given, it must be chosen from the EnumClass or else query will not return
        expected results
        """
        query = Payroll.query
        if status:
            query = query.filter_by(status=status)
            logger.debug(f"Fetching payrolls with status {status}")
        else:
            logger.info("Fetching all payrolls")
        return query.all()
    
    @staticmethod
    def get_by_id(payroll_id: int) -> Payroll | None:
        """get payroll by ID"""
        payroll = Payroll.query.get(payroll_id)
        if payroll:
            logger.info(f"Found payroll ID {payroll_id}")
        else:
            logger.warning(f"Payroll ID {payroll_id} not found")
        return payroll
       
    @staticmethod
    def update(payroll_id: int, **kwargs) -> Payroll | None:
        """
        update payroll attributes only if payroll is in DRAFT status.
        recalculate gross pay and net pay if start_date or end_date changed.

        allowed updates:
        - start_date (datetime)
        - end_date (datetime)
        """
        payroll = Payroll.query.get(payroll_id)
        if not payroll:
            logger.warning(f"Update failed: Payroll ID {payroll_id} not found")
            return None

        if payroll.status != PayrollStatusEnum.DRAFT:
            logger.warning(f"Update failed: Payroll ID {payroll_id} is not in DRAFT status")
            return None
        
        # track if date range changed (to know if we recalc)
        dates_changed = False
        try:
            for field in ['start_date', 'end_date']:
                if field in kwargs and kwargs[field] is not None:
                    old_value = getattr(payroll, field)
                    new_value = kwargs[field]
                    if old_value != new_value:
                        setattr(payroll, field, new_value)
                        logger.info(f"Updated payroll {field} from {old_value} to {new_value}")
                        dates_changed = True
            
            if dates_changed:

                from app.services.payroll_worklog_service import PayrollWorklogService
                payroll_worklogs = PayrollWorklogService.get_worklogs_for_payroll(payroll_id)

                filtered_data = [
                    payroll_worklog for payroll_worklog in payroll_worklogs
                    if payroll.start_date <= payroll_worklog.worklog.date <= payroll.end_date
                ]
                
                total_hours = sum(payroll_worklog.worklog.hours_worked for payroll_worklog in filtered_data)
                payroll.gross_pay = total_hours * payroll.employee.role.rate
                payroll.net_pay = payroll.gross_pay * (1 - payroll.organization.tax_rate)
                logger.info(f"Recalculated payroll totals after date update")

            db.session.commit()
            logger.info(f"Updated payroll ID {payroll_id}")
            return payroll
        
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to update payroll ID {payroll_id}: {str(e)}")
            raise

    @staticmethod
    def archive(payroll_id: int) -> bool:
        """
        **SEVERE ACTION**
        archive payroll only if it's already finalized

        archiving marks the payroll as inactive (soft delete)
        """
        payroll = Payroll.query.get(payroll_id)
        if not payroll:
            logger.warning(f"Archive failed: Payroll ID {payroll_id} not found")
            return False
        
        if payroll.status != PayrollStatusEnum.FINALIZED:
            logger.warning(f"Archive failed: Payroll ID {payroll_id} must be FINALIZED to archive")
            return False
        
        try:
            payroll.status = PayrollStatusEnum.ARCHIVED 
            payroll.archived_at = datetime.now(timezone.utc)
            db.session.commit()
            logger.info(f"Archived payroll ID {payroll_id}")
            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Failed to archive payroll ID {payroll_id}: {str(e)}")
            return False