from app.utils import get_logger
from app.extensions import db
from app.models import Organization

logger = get_logger(__name__)

"""

Organization Service does not need all of the CRUD
operations as it acts as a SINGLE ROW CONFIGURATION TABLE

NO DELETION, NO CREATION SHOULD BE ADDED

"""

class OrganizationService:

    @staticmethod
    def get():
        organization = Organization.query.first()
        if organization:
            logger.info(f"Fetched organization id '{organization.id}'")
        else:
            logger.info("No organization configuration found")
        return organization

    @staticmethod
    def update(org_id, 
               name=None, 
               total_salary_budget=None,
               budget_start_month=None,
               budget_start_day=None,
               budget_end_month=None,
               budget_end_day=None,
               tax_rate=None):

        organization = Organization.query.get(org_id)
        if not organization:
            logger.info(f"Update failed: No organization found with id '{org_id}'")
            return None

        if not any([
            name, total_salary_budget, budget_start_month, budget_start_day,
            budget_end_month, budget_end_day, tax_rate
        ]):
            logger.info(f"Tried updating organization id '{org_id}' with no fields provided")
            return None

        old_name = organization.name
        old_total_salary_budget = organization.total_salary_budget
        old_budget_start_month = organization.budget_start_month
        old_budget_start_day = organization.budget_start_day
        old_budget_end_month = organization.budget_end_month
        old_budget_end_day = organization.budget_end_day
        old_tax_rate = organization.tax_rate

        updates = {
            "name": name,
            "total_salary_budget": total_salary_budget,
            "budget_start_month": budget_start_month,
            "budget_start_day": budget_start_day,
            "budget_end_month": budget_end_month,
            "budget_end_day": budget_end_day,
            "tax_rate": tax_rate,
        }

        for attr, value in updates.items():
            if value is not None:
                setattr(organization, attr, value)

        try:
            db.session.commit()
            logger.info(f"Updated organization id '{org_id}'")

            if name:
                logger.info(f"Name '{old_name}' -> '{name}'")
            if total_salary_budget:
                logger.info(f"Total Salary Budget '${old_total_salary_budget}' -> '${total_salary_budget}'")
            if budget_start_month:
                logger.info(f"Budget Start Month '{old_budget_start_month}' -> '{budget_start_month}'")
            if budget_start_day:
                logger.info(f"Budget Start Day '{old_budget_start_day}' -> '{budget_start_day}'")
            if budget_end_month:
                logger.info(f"Budget End Month '{old_budget_end_month}' -> '{budget_end_month}'")
            if budget_end_day:
                logger.info(f"Budget End Day '{old_budget_end_day}' -> '{budget_end_day}'")
            if tax_rate:
                logger.info(f"Tax Rate '{old_tax_rate}' -> '{tax_rate}'")

            return organization

        except Exception as e:
            db.session.rollback()
            logger.exception(f"Error updating organization id '{org_id}'")
            raise