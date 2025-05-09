from flask import (
    render_template, 
    Blueprint,
    request,
    redirect,
    url_for,
    flash
)
from app.services import RoleService

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")

@roles_bp.route("/", methods=["GET"])
def index():
    roles = RoleService.get_all()
    return render_template("roles.html", roles=roles)