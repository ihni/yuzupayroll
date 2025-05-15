from flask import (
    render_template, 
    Blueprint,
)
from app.services import EmployeeService

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")

@employees_bp.route("/", methods=["GET"])
def index():
    employees = EmployeeService.get_all()
    return render_template("employees/index.html", employees=employees)