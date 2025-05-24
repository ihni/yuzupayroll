from app.extensions import db
from app.models import Payroll, PayrollStatusEnum
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from app.utils import get_logger

logger = get_logger(__name__)

class PayrollService:

    @staticmethod
    def create_payroll(employee_id: int, start_date: datetime, end_date: datetime) -> Payroll:
        """Creates a payroll shell from a valid employee id"""
        try:
            payroll = Payroll(employee_id=employee_id,
                              start_date=start_date,
                              end_date=end_date,
                              gross_pay=0.00,
                              net_pay=0.00,
                              status=PayrollStatusEnum.DRAFT)
            db.session.add(payroll)
            db.session.flush()
            logger.info(f"Created payroll ID {payroll.id}")
            return payroll
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Payroll creation failed: {str(e)}")
            raise

    @staticmethod
    def calculate_totals(payroll_id: int, worklogs_data: list[dict]) -> Payroll:
        """Calculates payroll totals from provided worklogs data"""
        payroll = Payroll.query.get(payroll_id)
        if not payroll:
            raise ValueError("Payroll not found")

        try:
            total_hours = sum(w['hours_worked'] for w in worklogs_data)
            payroll.gross_pay = total_hours * payroll.employee.role.rate
            payroll.net_pay = payroll.gross_pay * (1 - payroll.organization.tax_rate)
            db.session.commit()
            logger.info(f"Calculated totals for payroll ID {payroll_id}")
            return payroll
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception(f"Payroll calculation failed: {str(e)}")
            raise

    @staticmethod
    def finalize(payroll_id: int) -> bool:
        """Finalizes payroll after all checks are done"""
        payroll = Payroll.query.get(payroll_id)
        if not payroll:
            return False

        try:
            payroll.status = PayrollStatusEnum.FINALIZED
            payroll.finalized_at = datetime.now(timezone.utc)
            db.session.commit()
            logger.info(f"Finalized payroll ID {payroll_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.info(f"Failed to finalize payroll ID {payroll_id}")
            raise
    
    @staticmethod
    def get_all(status: PayrollStatusEnum = None) -> list[Payroll]:
        """Get all payrolls, optionally filtered by status"""
        query = Payroll.query
        if status:
            query = query.filter_by(status=status)
            logger.debug(f"Fetching payrolls with status {status}")
        else:
            logger.info("Fetching all payrolls")
        return query.all()
    
    @staticmethod
    def get_by_id(payroll_id: int) -> Payroll | None:
        """Get employee by ID"""
        payroll = Payroll.query.get(payroll_id)
        if payroll:
            logger.info(f"Found payroll ID {payroll_id}")
        else:
            logger.warning(f"Payroll ID {payroll_id} not found")
        return payroll
       
    @staticmethod
    # FOR UPDATE, SINCE THIS IS A SNAPSHOT, MAKE THIS ACTION SEVERE
    # TODO:
    # should only update the 
    # updating should only be allowed while in draft,
    # updating should also recalculate gross pay and total hours
    # should probaly also update the table in payroll worklogs but not in this service
    # should update only the start or end date??(idk yet)
    def update(payroll_id, **kwargs):
        pass

    @staticmethod
    # should be a severe action
    def archive(payroll_id):
        pass