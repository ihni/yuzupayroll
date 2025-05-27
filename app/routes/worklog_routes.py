from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    flash
)
from datetime import datetime
from app.services import WorklogService
from app.models import WorklogStatusEnum

worklogs_bp = Blueprint("worklogs", __name__, url_prefix="/worklogs")

def redirect_back():
    return redirect(request.referrer or url_for('worklogs.index'))

@worklogs_bp.route("/eligible", methods=["GET"])
def eligible_for_payroll():
    try:
        employee_id = int(request.args['employee_id'])
        start_date = datetime.strptime(request.args['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.args['end_date'], '%Y-%m-%d')
        payroll_id = request.args.get('payroll_id')

        worklogs = WorklogService.get_eligible_for_payroll(
            employee_id,
            start_date,
            end_date
        )
        return render_template(
            "worklogs/eligible.html",
            worklogs=worklogs,
            payroll_id=payroll_id,
            start_date=start_date.date(),
            end_date=end_date.date()
        )
    except (KeyError, ValueError):
        flash('Missing or invalid parameters', 'error')
        return redirect(url_for('payrolls.index'))

@worklogs_bp.route("/", methods=["GET"])
def index():
    status_filter = request.args.get('status', '').upper()
    if status_filter in WorklogStatusEnum.__members__:
        worklogs = WorklogService.get_all(status=WorklogStatusEnum[status_filter])
    else:
        worklogs = WorklogService.get_all()

    return render_template(
        "worklogs/index.html",
        worklogs=worklogs,
        status_filter=status_filter
    )

@worklogs_bp.route("/<int:worklog_id>/lock", methods=["POST"])
def lock(worklog_id):
    success = WorklogService.lock(worklog_id)
    flash("Worklog locked" if success else "Lock failed", "success" if success else "error")
    return redirect_back()

@worklogs_bp.route("/<int:worklog_id>/unlock", methods=["POST"])
def unlock(worklog_id):
    success = WorklogService.unlock(worklog_id)
    flash("Worklog unlocked" if success else "Unlock failed", "success" if success else "error")
    return redirect_back()

@worklogs_bp.route("/bulk-lock", methods=["POST"])
def bulk_lock():
    try:
        worklog_ids = [int(id) for id in request.form.getlist('worklog_ids')]
        if WorklogService.bulk_lock(worklog_ids):
            flash(f'{len(worklog_ids)} worklogs locked', 'success')
        else:
            flash('Bulk lock failed', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect_back()