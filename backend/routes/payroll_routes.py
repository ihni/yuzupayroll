from datetime import datetime
from typing import List, Optional
from flask import (
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
from backend.services import PayrollService, PayrollWorklogService, WorklogService
from backend.models import PayrollStatusEnum, WorklogStatusEnum

payrolls_bp = Blueprint(
    "payrolls",
    __name__,
    url_prefix="/payrolls",
)

def _redirect_to_payroll_details(payroll_id: int) -> Response:
    """helper to redirect to payroll details page"""
    return redirect(url_for('payrolls.details', payroll_id=payroll_id))

def _validate_draft_payroll(payroll_id: int) -> Optional[dict]:
    """validate payroll exists and is in DRAFT status"""
    payroll = PayrollService.get_by_id(payroll_id)
    if not payroll:
        flash('Payroll not found', 'error')
        abort(404)
    if payroll.status != PayrollStatusEnum.DRAFT:
        flash('Operation only allowed on DRAFT payrolls', 'error')
        return None
    return payroll

def _parse_date(date_str: str) -> datetime:
    """parse and validate date string"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise BadRequest("Invalid date format. Use YYYY-MM-DD")

@payrolls_bp.route("/", methods=["GET"])
def index() -> str:
    """list all payrolls with optional status filtering"""
    status_filter = request.args.get('status', '').upper()
    if status_filter in PayrollStatusEnum.__members__:
        payrolls = PayrollService.get_all(status=PayrollStatusEnum[status_filter])
    else:
        payrolls = PayrollService.get_all()
    
    return render_template(
        "payrolls/index.html",
        payrolls=payrolls,
        status_filter=status_filter,
        status_choices=PayrollStatusEnum
    )

@payrolls_bp.route("/create", methods=["GET", "POST"])
def create() -> Response | str:
    """create a new payroll"""
    if request.method == "GET":
        return render_template("payrolls/create.html")
    
    try:
        employee_id = int(request.form['employee_id'])
        start_date = _parse_date(request.form['start_date'])
        end_date = _parse_date(request.form['end_date'])
        
        if start_date >= end_date:
            flash('End date must be after start date', 'error')
            return render_template("payrolls/create.html", form_data=request.form)
        
        payroll = PayrollService.create_payroll(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date
        )
        flash('Payroll created successfully!', 'success')
        return _redirect_to_payroll_details(payroll.id)
    
    except (KeyError, BadRequest) as e:
        flash(str(e) or 'Missing required fields', 'error')
        return render_template("payrolls/create.html", form_data=request.form)
    except Exception as e:
        flash('Failed to create payroll', 'error')
        return render_template("payrolls/create.html", form_data=request.form)

@payrolls_bp.route("/<int:payroll_id>", methods=["GET"])
def details(payroll_id: int) -> str:
    """view payroll details"""
    payroll = PayrollService.get_by_id(payroll_id)
    if not payroll:
        flash('Payroll not found', 'error')
        abort(404)
    total_hours = sum(pw.hours_recorded for pw in payroll.payroll_worklogs)
    return render_template(
        "payrolls/details.html",
        payroll=payroll,
        total_hours=total_hours,
        PayrollStatusEnum=PayrollStatusEnum,
        WorklogStatusEnum=WorklogStatusEnum
    )

@payrolls_bp.route("/<int:payroll_id>/calculate", methods=["POST"])
def calculate(payroll_id: int) -> Response:
    """calculate payroll totals"""
    if not _validate_draft_payroll(payroll_id):
        return _redirect_to_payroll_details(payroll_id)

    try:
        PayrollService.calculate_totals(payroll_id)
        flash('Payroll calculated successfully!', 'success')
    except Exception as e:
        flash(f'Calculation failed: {str(e)}', 'error')

    return _redirect_to_payroll_details(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/finalize", methods=["POST"])
def finalize(payroll_id: int) -> Response:
    """finalize a payroll"""
    if not _validate_draft_payroll(payroll_id):
        return _redirect_to_payroll_details(payroll_id)

    try:
        if PayrollService.finalize(payroll_id):
            flash('Payroll finalized successfully!', 'success')
        else:
            flash('Finalization failed - check payroll details', 'error')
    except Exception as e:
        flash(f'System error during finalization: {str(e)}', 'error')

    return _redirect_to_payroll_details(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/add-worklogs", methods=["POST"])
def add_worklogs(payroll_id: int) -> Response:
    """add worklogs to payroll"""
    if not _validate_draft_payroll(payroll_id):
        return _redirect_to_payroll_details(payroll_id)

    try:
        worklog_ids = [int(id) for id in request.form.getlist('worklog_ids')]
        if not worklog_ids:
            flash('No worklogs selected', 'error')
            return _redirect_to_payroll_details(payroll_id)

        added_count = PayrollService.add_worklogs_to_payroll(payroll_id, worklog_ids)
        flash(f'Added {added_count} worklogs to payroll', 'success')
    except ValueError:
        flash('Invalid worklog IDs provided', 'error')
    except Exception as e:
        flash(f'Failed to add worklogs: {str(e)}', 'error')

    return _redirect_to_payroll_details(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/remove-worklog/<int:worklog_id>", methods=["POST"])
def remove_worklog(payroll_id: int, worklog_id: int) -> Response:
    """Remove worklog from payroll."""
    if not _validate_draft_payroll(payroll_id):
        return _redirect_to_payroll_details(payroll_id)

    try:
        if PayrollService.remove_worklogs_from_payroll(payroll_id, [worklog_id]):
            flash('Worklog removed successfully', 'success')
        else:
            flash('Failed to remove worklog', 'error')
    except Exception as e:
        flash(f'System error: {str(e)}', 'error')

    return _redirect_to_payroll_details(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/edit", methods=["GET", "POST"])
def edit(payroll_id: int) -> Response | str:
    """edit payroll details"""
    payroll = PayrollService.get_by_id(payroll_id)
    if not payroll:
        flash('Payroll not found', 'error')
        abort(404)
    
    if payroll.status != PayrollStatusEnum.DRAFT:
        flash('Only DRAFT payrolls can be edited', 'error')
        return _redirect_to_payroll_details(payroll_id)

    if request.method == "GET":
        return render_template("payrolls/edit.html", payroll=payroll)

    try:
        start_date = _parse_date(request.form['start_date'])
        end_date = _parse_date(request.form['end_date'])
        
        if start_date >= end_date:
            flash('End date must be after start date', 'error')
            return render_template("payrolls/edit.html", payroll=payroll)

        if PayrollService.update(payroll_id, start_date=start_date, end_date=end_date):
            flash('Payroll updated successfully', 'success')
        else:
            flash('Failed to update payroll', 'error')
    except (KeyError, BadRequest) as e:
        flash(str(e) or 'Invalid form data', 'error')
    except Exception as e:
        flash(f'System error: {str(e)}', 'error')

    return _redirect_to_payroll_details(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/lock-worklog/<int:worklog_id>", methods=["POST"])
def lock_worklog(payroll_id: int, worklog_id: int) -> Response:
    """Lock a worklog from payroll details"""
    if not _validate_draft_payroll(payroll_id):
        return _redirect_to_payroll_details(payroll_id)

    try:
        payroll = PayrollService.get_by_id(payroll_id)
        if not any(pw.worklog_id == worklog_id for pw in payroll.payroll_worklogs):
            flash("Worklog not found in this payroll", "error")
            return _redirect_to_payroll_details(payroll_id)

        if WorklogService.lock(worklog_id):
            flash("Worklog locked successfully", "success")
        else:
            flash("Failed to lock worklog", "error")
    except Exception as e:
        flash(f"Failed to lock worklog: {str(e)}", "error")
    
    return _redirect_to_payroll_details(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/unlock-worklog/<int:worklog_id>", methods=["POST"])
def unlock_worklog(payroll_id: int, worklog_id: int) -> Response:
    """Unlock a worklog from payroll details"""
    if not _validate_draft_payroll(payroll_id):
        return _redirect_to_payroll_details(payroll_id)

    try:
        payroll = PayrollService.get_by_id(payroll_id)
        if not any(pw.worklog_id == worklog_id for pw in payroll.payroll_worklogs):
            flash("Worklog not found in this payroll", "error")
            return _redirect_to_payroll_details(payroll_id)

        if WorklogService.unlock(worklog_id):
            flash("Worklog unlocked successfully", "success")
        else:
            flash("Failed to unlock worklog (may be in a finalized payroll)", "error")
    except Exception as e:
        flash(f"Failed to unlock worklog: {str(e)}", "error")
    
    return _redirect_to_payroll_details(payroll_id)