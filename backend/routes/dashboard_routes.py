from flask import Blueprint, render_template # type: ignore
from collections import defaultdict
from backend.extensions import db
from backend.services import PayrollService, OrganizationService
from backend.models import Role, PayrollWorklog, Worklog, Employee, RoleStatusEnum

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

def _get_net_salary_by_role():
    """
    Calculate total net salary grouped by active roles.
    Returns two lists: role names and corresponding net salary totals.
    """
    results = (
        db.session.query(
            Role.name,
            (PayrollWorklog.hours_recorded * Role.rate).label("net_salary")
        )
        .join(PayrollWorklog.worklog)
        .join(Worklog.employee)
        .join(Employee.role)
        .filter(Role.status == RoleStatusEnum.ACTIVE)
        .all()
    )

    role_totals = defaultdict(float)
    for role_name, net_salary in results:
        role_totals[role_name] += float(net_salary or 0.0)

    role_labels = list(role_totals.keys())
    role_net_totals = list(role_totals.values())
    return role_labels, role_net_totals

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
def dashboard():
    payrolls = PayrollService.get_all()
    org = OrganizationService.get()

    # Aggregate monthly totals for net and gross pay
    monthly_net_totals = defaultdict(float)
    monthly_gross_totals = defaultdict(float)
    for p in payrolls:
        month_key = p.created_at.strftime("%Y-%m")
        monthly_net_totals[month_key] += float(p.net_pay or 0)
        monthly_gross_totals[month_key] += float(p.gross_pay or 0)

    # Sort months for consistent chart x-axis
    sorted_months = sorted(monthly_net_totals.keys())
    net_totals = [monthly_net_totals[m] for m in sorted_months]
    gross_totals = [monthly_gross_totals[m] for m in sorted_months]

    # Count payroll statuses
    status_counts = defaultdict(int)
    for p in payrolls:
        status_counts[p.status.name] += 1

    # Get net salary by role for breakdown
    role_labels, role_net_totals = _get_net_salary_by_role()

    return render_template(
        "dashboard/index.html",
        months=sorted_months,
        net_totals=net_totals,
        gross_totals=gross_totals,
        status_labels=list(status_counts.keys()),
        status_data=list(status_counts.values()),
        org_name=org.name,
        fiscal_start=f"{org.budget_start_month}/{org.budget_start_day}",
        fiscal_end=f"{org.budget_end_month}/{org.budget_end_day}",
        role_labels=role_labels,
        role_net_totals=role_net_totals,
    )