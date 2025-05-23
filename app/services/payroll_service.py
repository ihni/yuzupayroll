from app.utils import get_logger
from app.extensions import db
from app.models import Payroll

logger = get_logger(__name__)

class PayrollService:

    @staticmethod
    def create(emp_id, pay_period_start, pay_period_end, gross_pay, total_hours):
        try:
            payroll = Payroll(
                employee_id=emp_id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end,
                gross_pay=gross_pay,
                total_hours=total_hours
            )
            db.session.add(payroll)
            db.session.commit()
            logger.info(f"Created payroll for employee id '{emp_id}'")
            return payroll
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Failed to create payroll for employee id '{emp_id}'")
            raise
    
    @staticmethod
    def get_all():
        payrolls = Payroll.query.all()
        logger.info(f"Fetched {len(payrolls)} payroll/s")
        return payrolls
    
    @staticmethod
    def get_all_active():
        payrolls = Payroll.query_not_deleted().all()
        logger.info(f"Fetched {len(payrolls)} active payroll/s")
        return payrolls
    
    @staticmethod
    def get_all_deleted():
        payrolls = Payroll.query_deleted().all()
        logger.info(f"Fetched {len(payrolls)} deleted payroll/s")
        return payrolls
    
    @staticmethod
    def get_by_id(payroll_id):
        payroll = Payroll.query.get(payroll_id)
        if payroll:
            logger.info(f"Found payroll id '{payroll_id}'")
        else:
            logger.info(f"No payroll found with id '{payroll_id}'")
        return payroll
    
    @staticmethod
    # FOR UPDATE, SINCE THIS IS A SNAPSHOT, MAKE THIS ACTION SEVERE
    # TODO:
    # should updating pay period be based from the worklogs or should it be
    # manually edited?
    # should gross pay and total hours be based from the worklogs or manually edited too?
    def update(payroll_id, pay_period_start=None, hours_worked=None):
        pass

    @staticmethod
    def delete(payroll_id):
        payroll = Payroll.query.get(payroll_id)
        if not work_log:
            logger.info(f"Delete failed: No payroll found with id '{payroll_id}'")
            return False

        if payroll.is_deleted:
            logger.info(f"Delete failed: payroll id '{payroll_id}' is already marked deleted")
            return False

        try:
            payroll.soft_delete()
            db.session.commit()
            logger.info(f"Deleted payroll id '{payroll_id}'")
            return True
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error deleting payroll id '{payroll_id}'")
            raise

    @staticmethod
    def restore(payroll_id):
        payroll = Payroll.query.get(payroll_id)
        if not payroll:
            logger.info(f"Restore failed: No payroll found with id '{payroll_id}'")
            return False
        
        if not payroll.is_deleted:
            logger.info(f"Restore failed: payroll id '{payroll_id}' is not marked deleted")
            return False
            
        try:
            payroll.restore()
            db.session.commit()
            logger.info(f"Restored payroll id '{payroll_id}'")
            return True
        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error restoring payroll id '{payroll_id}'")
            raise