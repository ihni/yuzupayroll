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
from backend.services import WorklogService
from backend.models import WorklogStatusEnum

worklogs_bp = Blueprint(
    "worklogs",
    __name__,
    url_prefix="/worklogs",
    template_folder="templates"
)

def _redirect_back(default_endpoint: str = 'worklogs.index') -> Response:
    """helper to redirect back or to default endpoint"""
    return redirect(request.referrer or url_for(default_endpoint))

def _get_valid_status_filter() -> Optional[WorklogStatusEnum]:
    """validate and return status filter from request args"""
    status_filter = request.args.get('status', '').upper()
    if status_filter in WorklogStatusEnum.__members__:
        return WorklogStatusEnum[status_filter]
    return None

def _parse_date(date_str: str) -> datetime:
    """parse date string with validation"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise BadRequest("Invalid date format. Use YYYY-MM-DD")

@worklogs_bp.route("/eligible", methods=["GET"])
def eligible_for_payroll() -> Response | str:
    """view worklogs eligible for payroll processing"""
    try:
        employee_id = int(request.args['employee_id'])
        start_date = _parse_date(request.args['start_date'])
        end_date = _parse_date(request.args['end_date'])
        payroll_id = request.args.get('payroll_id')

        worklogs = WorklogService.get_eligible_for_payroll(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date
        )

        return render_template(
            "worklogs/eligible.html",
            worklogs=worklogs,
            payroll_id=payroll_id,
            start_date=start_date.date(),
            end_date=end_date.date(),
            employee_id=employee_id
        )

    except (KeyError, BadRequest) as e:
        flash(str(e) or 'Missing required parameters', 'error')
        return redirect(url_for('payrolls.index'))
    except Exception as e:
        flash('Failed to retrieve eligible worklogs', 'error')
        abort(500)

@worklogs_bp.route("/", methods=["GET"])
def index() -> str:
    """list all worklogs with optional status filtering"""
    status_filter = _get_valid_status_filter()
    worklogs = WorklogService.get_all(status=status_filter)

    return render_template(
        "worklogs/index.html",
        worklogs=worklogs,
        status_filter=status_filter.value if status_filter else '',
        status_choices=WorklogStatusEnum
    )

@worklogs_bp.route("/<int:worklog_id>/lock", methods=["POST"])
def lock(worklog_id: int) -> Response:
    """lock a worklog to prevent modifications"""
    if not WorklogService.lock(worklog_id):
        flash('Lock failed - worklog not found or already locked', 'error')
        abort(404)
    
    flash('Worklog locked successfully', 'success')
    return _redirect_back()

@worklogs_bp.route("/<int:worklog_id>/unlock", methods=["POST"])
def unlock(worklog_id: int) -> Response:
    """unlock a worklog to allow modifications"""
    if not WorklogService.unlock(worklog_id):
        flash('Unlock failed - worklog not found or not locked', 'error')
        abort(404)
    
    flash('Worklog unlocked successfully', 'success')
    return _redirect_back()

@worklogs_bp.route("/bulk-lock", methods=["POST"])
def bulk_lock() -> Response:
    """lock multiple worklogs at once"""
    try:
        worklog_ids: List[int] = [int(id) for id in request.form.getlist('worklog_ids')]
        if not worklog_ids:
            flash('No worklogs selected', 'error')
            return _redirect_back()

        success_count = WorklogService.bulk_lock(worklog_ids)
        
        if success_count == len(worklog_ids):
            flash(f'Successfully locked {success_count} worklogs', 'success')
        elif success_count > 0:
            flash(f'Partially completed - locked {success_count} of {len(worklog_ids)} worklogs', 'warning')
        else:
            flash('Bulk lock failed - no worklogs were locked', 'error')

    except ValueError:
        flash('Invalid worklog IDs provided', 'error')
    except Exception as e:
        flash('System error during bulk operation', 'error')

    return _redirect_back()