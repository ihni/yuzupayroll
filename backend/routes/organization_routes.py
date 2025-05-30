from decimal import Decimal
from typing import Dict, Any
from flask import ( # type: ignore
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    abort,
    Response
)
from werkzeug.exceptions import BadRequest # type: ignore
from backend.services import OrganizationService

organization_bp = Blueprint(
    "organization",
    __name__,
    url_prefix="/organization",
    template_folder="templates"
)

def _validate_organization_exists() -> Dict[str, Any]:
    """ensure organization exists or return 404"""
    org = OrganizationService.get()
    if not org:
        flash('Organization configuration not found', 'error')
        abort(404)
    return org

def _parse_organization_form() -> Dict[str, Any]:
    """parse and validate organization form data"""
    try:
        return {
            'name': request.form['name'].strip(),
            'tax_rate': Decimal(request.form['tax_rate']),
            'total_salary_budget': Decimal(request.form['total_salary_budget']),
            'budget_start_month': int(request.form['budget_start_month']),
            'budget_start_day': int(request.form['budget_start_day']),
            'budget_end_month': int(request.form['budget_end_month']),
            'budget_end_day': int(request.form['budget_end_day'])
        }
    except (KeyError, ValueError) as e:
        raise BadRequest("Invalid form data: please check all fields")

@organization_bp.route("/", methods=["GET"])
def details() -> str:
    """view organization configuration"""
    org = OrganizationService.get()
    if not org:
        flash('Organization configuration not found', 'warning')
    return render_template("organization/details.html", org=org)

@organization_bp.route("/edit", methods=["GET", "POST"])
def edit() -> Response | str:
    """edit organization configuration"""
    org = _validate_organization_exists()
    
    if request.method == "GET":
        return render_template("organization/edit.html", org=org)
    
    try:
        update_data = _parse_organization_form()
        if not OrganizationService.update(**update_data):
            flash('Update failed - no changes made', 'error')
            return render_template("organization/edit.html", org=org)
        
        flash('Organization configuration updated successfully!', 'success')
        return redirect(url_for('organization.view'))
    
    except BadRequest as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f'System error: {str(e)}', 'error')
    
    return render_template("organization/edit.html", org=org)

@organization_bp.route("/reset-budget", methods=["POST"])
def reset_budget() -> Response:
    """reset salary budget to zero"""
    _validate_organization_exists()
    
    try:
        if OrganizationService.update(total_salary_budget=Decimal('0.00')):
            flash('Salary budget reset to zero successfully!', 'success')
        else:
            flash('Reset failed - no changes made', 'error')
    except Exception as e:
        flash(f'System error: {str(e)}', 'error')
    
    return redirect(url_for('organization.view'))