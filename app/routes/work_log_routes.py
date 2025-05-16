from flask import (
    render_template, 
    Blueprint,
    request,
    redirect,
    url_for,
)
from app.services import WorkLogService

work_logs_bp = Blueprint("work_logs", __name__, url_prefix="/work_logs")

@work_logs_bp.route("/", methods=["GET"])
def index():
    # all_logs = WorkLogService.get_all()
    active_logs = WorkLogService.get_all_active()
    deleted_logs = WorkLogService.get_all_deleted()
    return render_template('work_logs/index.html', active_logs=active_logs, deleted_logs=deleted_logs)


@work_logs_bp.route("/create", methods=["POST"])
def create_work_log():
    emp_id = request.form.get("employee_id")
    date_worked = request.form.get("date_worked")
    hours_worked = request.form.get("hours_worked")
    WorkLogService.create(
        emp_id=emp_id,
        date_worked=date_worked,
        hours_worked=hours_worked
    )
    return redirect(url_for("work_logs.index"))

@work_logs_bp.route("/update/<int:work_log_id>", methods=["POST"])
def update_work_log(work_log_id):
    date_worked = request.form.get("date_worked")
    hours_worked = request.form.get("hours_worked")

    date_worked = date_worked if date_worked else None
    hours_worked = float(hours_worked) if hours_worked else None

    WorkLogService.update(
        work_log_id=work_log_id,
        date_worked=date_worked,
        hours_worked= hours_worked,
    )
    return redirect(url_for("work_logs.index"))

@work_logs_bp.route("/delete/<int:work_log_id>", methods=["POST"])
def delete_work_log(work_log_id):
    WorkLogService.delete(work_log_id)
    return redirect(url_for("work_logs.index"))

@work_logs_bp.route('/restore/<int:work_log_id>/', methods=['POST'])
def restore_work_log(work_log_id):
    WorkLogService.restore(work_log_id)
    return redirect(url_for("work_logs.index"))