from app.extensions import db
from app.models import Organization
from sqlalchemy.exc import SQLAlchemyError # type: ignore
from app.utils import get_logger

logger = get_logger(__name__)

class OrganizationService:
    """

    organization service does not need all the CRUD
    operations as it acts as a SINGLE ROW CONFIGURATION TABLE

    NO DELETION, NO CREATION SHOULD BE ADDED

    """

    @staticmethod
    def get() -> Organization | None:
        """get the organization config"""
        org = Organization.query.first()
        if org:
            logger.debug("Fetched organization config")
        else:
            logger.error("No organization config found")
        return org

    @staticmethod
    def update(**kwargs) -> Organization | None:
        """
        update organization configuration

        args:
            **kwargs: attributes to update
                - name (str)
                - total_salary_budget (Decimal)
                - budget_start_month (int 1-12)
                - budget_start_day (int 1-31)
                - budget_end_month (int 1-12) 
                - budget_end_day (int 1-31)
                - tax_rate (Decimal 0-1)
        """
        
        if not kwargs:
            logger.warning("Update aborted: No fields provided")
            return None

        org = Organization.query.first()
        if not org:
            logger.warning("No organization config found to update")
            return None

        try:
            changes = False
            for key, value in kwargs.items():
                if hasattr(org, key) and value is not None:
                    old_value = getattr(org, key)
                    if old_value != value:
                        setattr(org, key, value)
                        logger.debug(f"Updating {key} from {old_value} to {value}")
                        changes = True

            if not changes:
                logger.info("No changes detected in organization config")
                return org
                
            db.session.commit()
            logger.info("Updated organization config")
            return org
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception("Failed to update organization config")
            raise