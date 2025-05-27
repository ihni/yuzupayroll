from flask import (
    render_template, 
    Blueprint,
    request,
    redirect,
    url_for,
    flash
)
from app.services import PayrollService, PayrollWorklogService, WorklogService
from app.models import PayrollStatusEnum, WorklogStatusEnum
from datetime import datetime

payrolls_bp = Blueprint("payrolls", __name__, url_prefix="/payrolls")

def redirect_back_to_view(payroll_id):
    return redirect(url_for('payrolls.view', payroll_id=payroll_id))

@payrolls_bp.route("/", methods=["GET"])
def index():
    status_filter = request.args.get('status')
    
    if status_filter and status_filter.upper() in PayrollStatusEnum.__members__:
        payrolls = PayrollService.get_all(status=PayrollStatusEnum[status_filter.upper()])
    else:
        payrolls = PayrollService.get_all()
    
    return render_template("payrolls/index.html",
                         payrolls=payrolls,
                         status_filter=status_filter)

@payrolls_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            employee_id = int(request.form['employee_id'])
            start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
            
            if start_date >= end_date:
                flash('End date must be after start date', 'error')
                return redirect(url_for('payrolls.create'))
            
            payroll = PayrollService.create_payroll(
                employee_id=employee_id,
                start_date=start_date,
                end_date=end_date
            )
            flash('Payroll created successfully!', 'success')
            return redirect(url_for('payrolls.view', payroll_id=payroll.id))
        except ValueError as e:
            flash('Invalid date format or employee ID', 'error')
        except Exception as e:
            flash(f'Error creating payroll: {str(e)}', 'error')
    
    return render_template("payrolls/create.html")

@payrolls_bp.route("/<int:payroll_id>", methods=["GET"])
def view(payroll_id):
    payroll = PayrollService.get_by_id(payroll_id)
    if not payroll:
        flash('Payroll not found', 'error')
        return redirect(url_for('payrolls.index'))
    
    return render_template("payrolls/view.html",
                         payroll=payroll,
                         PayrollStatusEnum=PayrollStatusEnum,
                         WorklogStatusEnum=WorklogStatusEnum,)

@payrolls_bp.route("/<int:payroll_id>/calculate", methods=["POST"])
def calculate(payroll_id):
    payroll = PayrollService.get_by_id(payroll_id)
    if not payroll or payroll.status != PayrollStatusEnum.DRAFT:
        flash('Cannot calculate this payroll', 'error')
        return redirect_back_to_view(payroll_id)

    try:
        PayrollService.calculate_totals(payroll_id)
        flash('Payroll calculated successfully!', 'success')
    except Exception as e:
        flash(f'Calculation failed: {e}', 'error')

    return redirect_back_to_view(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/finalize", methods=["POST"])
def finalize(payroll_id):
    payroll = PayrollService.get_by_id(payroll_id)
    if not payroll or payroll.status != PayrollStatusEnum.DRAFT:
        flash('Cannot finalize this payroll', 'error')
        return redirect_back_to_view(payroll_id)

    try:
        if PayrollService.finalize(payroll_id):
            flash('Payroll finalized!', 'success')
        else:
            flash('Finalization failed', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')

    return redirect_back_to_view(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/add-worklogs", methods=["POST"])
def add_worklogs(payroll_id):
    try:
        worklog_ids = [int(id) for id in request.form.getlist('worklog_ids')]
        PayrollService.add_worklogs_in_payroll(payroll_id, worklog_ids)
        flash("Worklogs added and totals updated", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect_back_to_view(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/remove-worklog/<int:worklog_id>", methods=["POST"])
def remove_worklog(payroll_id, worklog_id):
    try:
        PayrollService.remove_worklogs_in_payroll(payroll_id, [worklog_id])
        flash("Worklog removed and totals updated", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect_back_to_view(payroll_id)

@payrolls_bp.route('/<int:payroll_id>/worklogs/<int:worklog_id>/lock', methods=['POST'])
def lock_worklog(payroll_id, worklog_id):
    try:
        success = PayrollService.lock_worklog_in_payroll(payroll_id, worklog_id)
        if success:
            flash("Worklog locked.", "success")
        else:
            flash("Could not lock worklog.", "warning")
    except Exception as e:
        flash(f"Error locking worklog: {str(e)}", "error")

    return redirect_back_to_view(payroll_id)

@payrolls_bp.route('/<int:payroll_id>/worklogs/<int:worklog_id>/unlock', methods=['POST'])
def unlock_worklog(payroll_id, worklog_id):
    try:
        success = PayrollService.unlock_worklog_in_payroll(payroll_id, worklog_id)
        if success:
            flash("Worklog unlocked.", "success")
        else:
            flash("Could not unlock worklog.", "warning")
    except Exception as e:
        flash(f"Error unlocking worklog: {str(e)}", "error")

    return redirect_back_to_view(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/edit", methods=["GET", "POST"])
def edit_payroll(payroll_id):
    payroll = PayrollService.get_by_id(payroll_id)
    if not payroll:
        flash("Payroll not found.", "error")
        return redirect(url_for("payrolls.list_payrolls"))

    if payroll.status != PayrollStatusEnum.DRAFT:
        flash("Only DRAFT payrolls can be edited.", "warning")
        return redirect_back_to_view(payroll_id)

    if request.method == "POST":
        try:
            start_date_str = request.form.get("start_date")
            end_date_str = request.form.get("end_date")
            # Parse dates from form strings, example format: 'YYYY-MM-DD'
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            updated_payroll = PayrollService.update(payroll_id, start_date=start_date, end_date=end_date)
            if updated_payroll:
                flash("Payroll updated successfully.", "success")
            else:
                flash("Failed to update payroll.", "error")
        except Exception as e:
            flash(f"Error updating payroll: {str(e)}", "error")

        return redirect_back_to_view(payroll_id)

    # GET method: render edit form
    return render_template("payrolls/edit.html", payroll=payroll)
