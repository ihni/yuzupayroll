from flask import ( # type: ignore
    render_template,
    Blueprint,
    request,
    redirect,
    abort,
    Response,
    url_for,
    flash
)
from werkzeug.exceptions import BadRequest # type: ignore
from typing import Optional, Dict, Any
from backend.services import EmployeeService
from backend.models import EmployeeStatusEnum

employees_bp = Blueprint(
    "employees", 
    __name__, 
    url_prefix="/employees"
)

def _redirect_back(default_endpoint: str = 'employees.index') -> Response:
    """helper function to redirect back to previous page or default endpoint"""
    return redirect(request.referrer or url_for(default_endpoint))

def _get_status_filter() -> Optional[EmployeeStatusEnum]:
    """get and validate status filter from request args"""
    status_filter = request.args.get('status')
    if status_filter and status_filter.upper() in EmployeeStatusEnum.__members__:
        return EmployeeStatusEnum[status_filter.upper()]
    return None

@employees_bp.route("/", methods=["GET"])
def index():
    """
    list all employees with optional status filtering
    
    query params:
        status (str): optional filter by employee status
    """
    status_filter = _get_status_filter()
    employees = EmployeeService.get_all(status=status_filter)

    return render_template(
        "employees/index.html",
        employees=employees,
        status_filter=status_filter.value if status_filter else None,
        status_choices=EmployeeStatusEnum
    )

@employees_bp.route("/create", methods=["GET", "POST"])
def create() -> Response | str:
    """create a new employee"""
    if request.method == "GET":
        return render_template("employees/create.html")
    
    try:
        form_data = {
            'first_name': request.form['first_name'].strip(),
            'last_name': request.form['last_name'].strip(),
            'email': request.form['email'].strip().lower(),
            'role_id': int(request.form['role_id'])
        }

        employee = EmployeeService.create(**form_data)
        if not employee:
            flash('Email already exists', 'error')
            return render_template("employees/create.html", form_data=form_data)
        
        flash('Employee created successfully!', 'success')
        return redirect(url_for('employees.details', emp_id=employee.id))
    
    except (KeyError, ValueError) as e:
        flash('Invalid form data: please check all fields', 'error')
        return render_template(
            "employees/create.html",
            form_data=request.form
        )
    except Exception as e:
        flash(f'System error: {str(e)}', 'error')
        return render_template(
            "employees/create.html",
            form_data=request.form
        )

@employees_bp.route("/<int:emp_id>", methods=["GET"])
def details(emp_id: int) -> str:
    """view employee details"""
    employee = EmployeeService.get_by_id(emp_id)
    if not employee:
        flash('Employee not found', 'error')
        abort(404)
        
    return render_template("employees/details.html", employee=employee)

@employees_bp.route("/<int:emp_id>/edit", methods=["GET", "POST"])
def edit(emp_id: int) -> Response | str:
    """Edit employee information."""
    employee = EmployeeService.get_by_id(emp_id)
    if not employee:
        flash('Employee not found', 'error')
        abort(404)
    
    if request.method == "GET":
        return render_template(
            "employees/edit.html",
            employee=employee,
            statuses=EmployeeStatusEnum
        )
    
    try:
        update_data: Dict[str, Any] = {
            'first_name': request.form['first_name'].strip(),
            'last_name': request.form['last_name'].strip(),
            'email': request.form['email'].strip().lower(),
            'role_id': int(request.form['role_id']),
            'status': EmployeeStatusEnum[request.form['status']]
        }
        
        updated_employee = EmployeeService.update(emp_id, **update_data)
        if not updated_employee:
            flash('Update failed - email may be in use or employee archived', 'error')
            return render_template(
                "employees/edit.html",
                employee=employee,
                statuses=EmployeeStatusEnum
            )
        
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('employees.details', emp_id=emp_id))
    
    except (KeyError, ValueError) as e:
        flash('Invalid form data: please check all fields', 'error')
    except Exception as e:
        flash(f'System error: {str(e)}', 'error')
    
    return render_template(
        "employees/edit.html",
        employee=employee,
        statuses=EmployeeStatusEnum
    )

@employees_bp.route("/<int:emp_id>/archive", methods=["POST"])
def archive(emp_id: int) -> Response:
    """archive an employee"""
    if not EmployeeService.archive(emp_id):
        flash('Archive failed - employee not found or already archived', 'error')
        abort(404)
    
    flash('Employee archived successfully', 'success')
    return _redirect_back()

@employees_bp.route("/<int:emp_id>/restore", methods=["POST"])
def restore(emp_id: int) -> Response:
    """restore an archived employee"""
    if not EmployeeService.restore(emp_id):
        flash('Restore failed - employee not found or not archived', 'error')
        abort(404)
    
    flash('Employee restored successfully', 'success')
    return _redirect_back()