from flask import Blueprint, render_template
from app.extensions import db
from collections import defaultdict
from app.services import PayrollService, OrganizationService
from app.models import Role, PayrollWorklog, Worklog, Employee, RoleStatusEnum
from sqlalchemy.orm import joinedload
from sqlalchemy import select

def get_net_salary_by_role():
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

@dashboard_bp.route('/')
def dashboard():
    payrolls = PayrollService.get_all()
    org = OrganizationService.get()
    monthly_net_totals = defaultdict(float)
    monthly_gross_totals = defaultdict(float)

    for p in payrolls:
        month_key = p.created_at.strftime("%Y-%m")
        net_pay_value = float(p.net_pay) if p.net_pay is not None else 0.0
        gross_pay_value = float(p.gross_pay) if p.gross_pay is not None else 0.0
        monthly_net_totals[month_key] += net_pay_value
        monthly_gross_totals[month_key] += gross_pay_value

    sorted_months = sorted(monthly_net_totals.keys())
    net_totals = [monthly_net_totals[m] for m in sorted_months]
    gross_totals = [monthly_gross_totals[m] for m in sorted_months]

    # Status counts
    status_counts = defaultdict(int)
    for p in payrolls:
        status_counts[p.status.name] += 1

    role_labels, role_net_totals = get_net_salary_by_role()

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
        role_net_totals=role_net_totals
    )