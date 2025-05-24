from flask import (
    render_template, 
    Blueprint,
    request,
    redirect,
    url_for,
    flash
)
from app.services import PayrollService, PayrollWorklogService
from app.models import PayrollStatusEnum
from datetime import datetime

payrolls_bp = Blueprint("payrolls", __name__, url_prefix="/payrolls")

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
                         payroll=payroll)

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
        flash(f'Calculation failed: {str(e)}', 'error')
    
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
        flash(f'Error: {str(e)}', 'error')
    
    return redirect_back_to_view(payroll_id)

@payrolls_bp.route("/<int:payroll_id>/add-worklogs", methods=["POST"])
def add_worklogs(payroll_id):
    try:
        worklog_ids = [int(id) for id in request.form.getlist('worklog_ids')]
        if PayrollWorklogService.bulk_create_associations(payroll_id, worklog_ids):
            flash('Worklogs added successfully!', 'success')
        else:
            flash('Some worklogs could not be added', 'warning')
    except Exception as e:
        flash(f'Error adding worklogs: {str(e)}', 'error')
    
    return redirect_back_to_view(payroll_id)

def redirect_back_to_view(payroll_id):
    return redirect(url_for('payrolls.view', payroll_id=payroll_id))