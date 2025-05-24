from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    flash
)
from app.services import OrganizationService
from decimal import Decimal

organization_bp = Blueprint("organization", __name__, url_prefix="/organization")

@organization_bp.route("/", methods=["GET"])
def view():
    org = OrganizationService.get()
    if not org:
        flash('Organization configuration not found', 'error')
    return render_template("organization/view.html", org=org)

@organization_bp.route("/edit", methods=["GET", "POST"])
def edit():
    org = OrganizationService.get()
    if not org:
        flash('Organization configuration not found', 'error')
        return redirect(url_for('organization.view'))
    
    if request.method == "POST":
        try:
            update_data = {
                'name': request.form['name'],
                'tax_rate': Decimal(request.form['tax_rate']),
                'total_salary_budget': Decimal(request.form['total_salary_budget']),
                'budget_start_month': int(request.form['budget_start_month']),
                'budget_start_day': int(request.form['budget_start_day']),
                'budget_end_month': int(request.form['budget_end_month']),
                'budget_end_day': int(request.form['budget_end_day'])
            }
            
            updated_org = OrganizationService.update(**update_data)
            if updated_org:
                flash('Organization configuration updated!', 'success')
                return redirect(url_for('organization.view'))
            else:
                flash('Update failed', 'error')
        except (ValueError, KeyError) as e:
            flash('Invalid form data', 'error')
        except Exception as e:
            flash(f'Error updating configuration: {str(e)}', 'error')
    
    return render_template("organization/edit.html", org=org)

@organization_bp.route("/reset-budget", methods=["POST"])
def reset_budget():
    try:
        updated_org = OrganizationService.update(
            total_salary_budget=Decimal('0.00')
        )
        if updated_org:
            flash('Salary budget reset to zero!', 'success')
        else:
            flash('Reset failed', 'error')
    except Exception as e:
        flash(f'Error resetting budget: {str(e)}', 'error')
    
    return redirect(url_for('organization.view'))