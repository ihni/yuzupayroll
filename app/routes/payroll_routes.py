from flask import (
    render_template, 
    Blueprint,
)
from app.services import PayrollService

payrolls_bp = Blueprint("payrolls", __name__, url_prefix="/payrolls")

@payrolls_bp.route("/", methods=["GET"])
def index():
    active_payrolls = PayrollService.get_all_active()
    deleted_payrolls = PayrollService.get_all_deleted()
    return render_template("payrolls/index.html", active_payrolls=active_payrolls)