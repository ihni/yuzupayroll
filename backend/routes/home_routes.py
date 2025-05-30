from flask import Blueprint, render_template # type: ignore

home_bp = Blueprint('index', __name__)

@home_bp.route('/')
def index():
    return render_template("home/index.html")