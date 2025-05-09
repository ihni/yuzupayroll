from flask import (
    render_template, 
    Blueprint,
    request,
    redirect,
    url_for,
    flash
)
from ..services import RoleService
from ..models import Role
from decimal import Decimal
import datetime
from ..utils import get_logger

logger = get_logger(__name__)

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")

@roles_bp.route('/')
def list_roles():
    roles_data = RoleService.get_all()
    counts_data = {
        role_id: RoleService.get_count_emp_by_role_id(role_id)['count']
        for role_id in (role['id'] for role in roles_data)
    }
    full_roles_details = [{
        "id": role['id'],
        "name": role['name'],
        "hourly_rate": role['hourly_rate'], 
        "total_employees": counts_data.get(role['id'], 0)
    } for role in roles_data]
    
    return render_template(
        "roles.html",
        full_roles_details=full_roles_details
    )

@roles_bp.route("/create", methods=["POST"])
def create_role():
    try:
        name = request.form["name"].strip()
        rate = Decimal(request.form["hourly_rate"])
        
        role = Role(name=name, hourly_rate=rate)
        
        role_id = RoleService.create(role)
        
        if role_id:
            flash("Role created successfully!", "success")
            return redirect(url_for("roles.list_roles"))
            
    except ValueError as e:
        flash(f"Invalid input: {str(e)}", "error")
    except Exception as e:
        flash("Failed to create role", "error")
        logger.error(f"Role creation failed: {str(e)}")
    
    return redirect(url_for("roles.list_roles"))