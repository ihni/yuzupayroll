from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    flash
)
from app.services import RoleService
from app.models import RoleStatusEnum

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")

@roles_bp.route("/", methods=["GET"])
def index():
    status_filter = request.args.get('status')
    
    if status_filter and status_filter.upper() in RoleStatusEnum.__members__:
        roles = RoleService.get_all(status=RoleStatusEnum[status_filter.upper()])
    else:
        roles = RoleService.get_all()
    
    return render_template("roles/index.html",
                         roles=roles,
                         status_filter=status_filter)

@roles_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            role = RoleService.create(
                name=request.form['name'],
                rate=float(request.form['rate'])
            )
            
            if role:
                flash('Role created successfully!', 'success')
                return redirect(url_for('roles.view', role_id=role.id))
            else:
                flash('Role name already exists', 'error')
        except ValueError:
            flash('Invalid rate value', 'error')
        except Exception as e:
            flash(f'Error creating role: {str(e)}', 'error')
    
    return render_template("roles/create.html")

@roles_bp.route("/<int:role_id>", methods=["GET"])
def view(role_id):
    role = RoleService.get_by_id(role_id)
    if not role:
        flash('Role not found', 'error')
        return redirect(url_for('roles.index'))
    
    return render_template("roles/view.html",
                         role=role)

@roles_bp.route("/<int:role_id>/edit", methods=["GET", "POST"])
def edit(role_id):
    role = RoleService.get_by_id(role_id)
    if not role:
        flash('Role not found', 'error')
        return redirect(url_for('roles.index'))
    
    if request.method == "POST":
        try:
            update_data = {
                'name': request.form['name'],
                'rate': float(request.form['rate']),
                'status': RoleStatusEnum[request.form['status']]
            }
            
            updated_role = RoleService.update(role_id, **update_data)
            if updated_role:
                flash('Role updated successfully!', 'success')
                return redirect(url_for('roles.view', role_id=role_id))
            else:
                flash('Update failed - name may be in use', 'error')
        except (ValueError, KeyError):
            flash('Invalid form data', 'error')
        except Exception as e:
            flash(f'Error updating role: {str(e)}', 'error')
    
    return render_template("roles/edit.html",
                         role=role,
                         statuses=RoleStatusEnum)

@roles_bp.route("/<int:role_id>/archive", methods=["POST"])
def archive(role_id):
    if RoleService.archive(role_id):
        flash('Role archived', 'success')
    else:
        flash('Archive failed - role not found or assigned to employees', 'error')
    return redirect_back()

@roles_bp.route("/<int:role_id>/restore", methods=["POST"])
def restore(role_id):
    if RoleService.restore(role_id):
        flash('Role restored', 'success')
    else:
        flash('Restore failed - role not found or not archived', 'error')
    return redirect_back()

def redirect_back():
    return redirect(request.referrer or url_for('roles.index'))