from flask import (
    render_template, 
    Blueprint,
    request,
    redirect,
    url_for,
)
from app.services import RoleService

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")

@roles_bp.route("/", methods=["GET"])
def index():
    roles = RoleService.get_all()
    return render_template("roles/index.html", roles=roles)

@roles_bp.route("/create", methods=["POST"])
def create_role():
    name = request.form.get("name")
    hourly_rate = request.form.get("hourly_rate")
    RoleService.create(name, hourly_rate)
    return redirect(url_for("roles.index"))

@roles_bp.route("/update/<int:role_id>", methods=["POST"])
def update_role(role_id):
    name = request.form.get("name")
    hourly_rate = request.form.get("hourly_rate")
    RoleService.update(
        role_id=role_id,
        name=name,
        hourly_rate=hourly_rate
    )
    return redirect(url_for("roles.index"))

@roles_bp.route("/delete/<int:role_id>", methods=["POST"])
def delete_role(role_id):
    RoleService.delete(role_id)
    return redirect(url_for("roles.index"))