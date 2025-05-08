from flask import (
    render_template, 
    Blueprint,
    request,
    redirect,
    url_for,
)
from ..services import RoleService
from ..models import Role
roles_bp = Blueprint("roles", __name__, url_prefix="/roles")

@roles_bp.route('/')
def list_roles():
    roles = RoleService.get_all()
    full_roles_details = []
    for role in roles:
        total_employees = RoleService.get_count_emp_by_role_id(role.id)
        full_roles_details.append = {
            "id": role.id,
            "name": role.name,
            "hourly_rate": role.hourly_rate, 
            "total_employees": total_employees,
        }
        
    return render_template(
        "roles.html",
        full_roles_details=full_roles_details
    )

@roles_bp.route("/create", methods=["POST"])
def create_role():
    name = request.form["name"]
    rate = request.form["hourly_rate"]
    result = RoleService.create(
        Role(name=name, hourly_rate=rate)
    )
    if result:
        return redirect(url_for("roles.list_roles"))
    else:
        pass # pass an error message here
