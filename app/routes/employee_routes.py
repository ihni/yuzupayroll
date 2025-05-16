from flask import (
    render_template, 
    Blueprint,
)
from app.services import EmployeeService

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")

@employees_bp.route("/", methods=["GET"])
def index():
    active_employees = EmployeeService.get_all_active()
    deleted_employees = EmployeeService.get_all_deleted()
    return render_template("employees/index.html", active_employees=active_employees)