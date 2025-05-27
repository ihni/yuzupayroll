from flask import ( # type: ignore
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    flash
)
from app.services import EmployeeService
from app.models import EmployeeStatusEnum

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")

def redirect_back(default='employees.index'):
    return redirect(request.referrer or url_for(default))

@employees_bp.route("/", methods=["GET"])
def index():
    status_filter = request.args.get('status')
    if status_filter and status_filter.upper() in EmployeeStatusEnum.__members__:
        employees = EmployeeService.get_all(status=EmployeeStatusEnum[status_filter.upper()])
    else:
        employees = EmployeeService.get_all()
    return render_template("employees/index.html", employees=employees, status_filter=status_filter)

@employees_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            employee = EmployeeService.create(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                role_id=int(request.form['role_id'])
            )
            if employee:
                flash('Employee created successfully!', 'success')
                return redirect(url_for('employees.view', emp_id=employee.id))
            flash('Email already exists', 'error')
        except ValueError:
            flash('Invalid role ID', 'error')
        except Exception as e:
            flash(f'Error creating employee: {str(e)}', 'error')
    
    return render_template("employees/create.html")

@employees_bp.route("/<int:emp_id>", methods=["GET"])
def view(emp_id):
    employee = EmployeeService.get_by_id(emp_id)
    if not employee:
        flash('Employee not found', 'error')
        return redirect(url_for('employees.index'))
    return render_template("employees/view.html", employee=employee)

@employees_bp.route("/<int:emp_id>/edit", methods=["GET", "POST"])
def edit(emp_id):
    employee = EmployeeService.get_by_id(emp_id)
    if not employee:
        flash('Employee not found', 'error')
        return redirect(url_for('employees.index'))
    
    if request.method == "POST":
        try:
            update_data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'role_id': int(request.form['role_id']),
                'status': EmployeeStatusEnum[request.form['status']]
            }
            updated_employee = EmployeeService.update(emp_id, **update_data)
            if updated_employee:
                flash('Employee updated successfully!', 'success')
                return redirect(url_for('employees.view', emp_id=emp_id))
            flash('Update failed - email may be in use or employee archived', 'error')
        except (ValueError, KeyError):
            flash('Invalid form data', 'error')
        except Exception as e:
            flash(f'Error updating employee: {str(e)}', 'error')
    
    return render_template("employees/edit.html", employee=employee, statuses=EmployeeStatusEnum)

@employees_bp.route("/<int:emp_id>/archive", methods=["POST"])
def archive(emp_id):
    if EmployeeService.archive(emp_id):
        flash('Employee archived', 'success')
    else:
        flash('Archive failed - employee not found or already archived', 'error')
    return redirect_back()

@employees_bp.route("/<int:emp_id>/restore", methods=["POST"])
def restore(emp_id):
    if EmployeeService.restore(emp_id):
        flash('Employee restored', 'success')
    else:
        flash('Restore failed - employee not found or not archived', 'error')
    return redirect_back()