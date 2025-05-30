from typing import Optional, Dict, Any
from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
    abort,
    Response
)
from werkzeug.exceptions import BadRequest # type: ignore
from backend.services import RoleService
from backend.models import RoleStatusEnum

roles_bp = Blueprint(
    "roles", 
    __name__, 
    url_prefix="/roles",
    template_folder="templates"
)

def _redirect_back(default_endpoint: str = 'roles.index') -> Response:
    """helper to redirect back or to default endpoint"""
    return redirect(request.referrer or url_for(default_endpoint))

def _get_valid_status_filter() -> Optional[RoleStatusEnum]:
    """validate and return status filter from request args"""
    status_filter = request.args.get('status', '').upper()
    if status_filter in RoleStatusEnum.__members__:
        return RoleStatusEnum[status_filter]
    return None

@roles_bp.route("/", methods=["GET"])
def index() -> str:
    """list roles with optional status filtering"""
    status_filter = _get_valid_status_filter()
    roles = RoleService.get_all(status=status_filter)
    
    return render_template(
        "roles/index.html",
        roles=roles,
        status_filter=status_filter.value if status_filter else '',
        status_choices=RoleStatusEnum
    )

@roles_bp.route("/create", methods=["GET", "POST"])
def create() -> Response | str:
    """create a new role"""
    if request.method == "GET":
        return render_template("roles/create.html")
    
    try:
        form_data = {
            'name': request.form['name'].strip(),
            'rate': float(request.form['rate'])
        }
        
        role = RoleService.create(**form_data)
        if not role:
            flash('Role name already exists', 'error')
            return render_template("roles/create.html", form_data=form_data)
        
        flash('Role created successfully!', 'success')
        return redirect(url_for('roles.details', role_id=role.id))
    
    except ValueError as e:
        flash('Invalid rate value' if 'rate' in str(e) else 'Invalid form data', 'error')
        return render_template("roles/create.html", form_data=request.form)
    except Exception as e:
        flash(f'System error: {str(e)}', 'error')
        return render_template("roles/create.html", form_data=request.form)

@roles_bp.route("/<int:role_id>", methods=["GET"])
def details(role_id: int) -> str:
    """view role details"""
    role = RoleService.get_by_id(role_id)
    if not role:
        flash('Role not found', 'error')
        abort(404)
        
    return render_template("roles/details.html", role=role)

@roles_bp.route("/<int:role_id>/edit", methods=["GET", "POST"])
def edit(role_id: int) -> Response | str:
    """edit role information"""
    role = RoleService.get_by_id(role_id)
    if not role:
        flash('Role not found', 'error')
        abort(404)
    
    if request.method == "GET":
        return render_template(
            "roles/edit.html",
            role=role,
            statuses=RoleStatusEnum
        )
    
    try:
        update_data: Dict[str, Any] = {
            'name': request.form['name'].strip(),
            'rate': float(request.form['rate']),
            'status': RoleStatusEnum[request.form['status']]
        }
        
        updated_role = RoleService.update(role_id, **update_data)
        if not updated_role:
            flash('Update failed - name may be in use', 'error')
            return render_template(
                "roles/edit.html",
                role=role,
                statuses=RoleStatusEnum
            )
        
        flash('Role updated successfully!', 'success')
        return redirect(url_for('roles.details', role_id=role_id))
    
    except (ValueError, KeyError) as e:
        flash('Invalid form data: please check all fields', 'error')
    except Exception as e:
        flash(f'System error: {str(e)}', 'error')
    
    return render_template(
        "roles/edit.html",
        role=role,
        statuses=RoleStatusEnum
    )

@roles_bp.route("/<int:role_id>/archive", methods=["POST"])
def archive(role_id: int) -> Response:
    """archive a role"""
    if not RoleService.archive(role_id):
        flash('Archive failed - role not found or assigned to employees', 'error')
        abort(404)
    
    flash('Role archived successfully', 'success')
    return _redirect_back()

@roles_bp.route("/<int:role_id>/restore", methods=["POST"])
def restore(role_id: int) -> Response:
    """restore an archived role"""
    if not RoleService.restore(role_id):
        flash('Restore failed - role not found or not archived', 'error')
        abort(404)
    
    flash('Role restored successfully', 'success')
    return _redirect_back()