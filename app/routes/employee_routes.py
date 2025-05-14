from flask import (
    render_template, 
    Blueprint,
)
from app.services import EmployeeService
from app.services import RoleService

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")

@employees_bp.route("/", methods=["GET"])
def index():
    roles = []
    employees = EmployeeService.get_all()

    # TODO: fix whatever this is
    # is this a good way of getting it???
    for employee in employees:
        roles.append(RoleService.get_by_id)
        
    return render_template(
        "employees.html", 
        employees=employees,
        roles=roles
    )