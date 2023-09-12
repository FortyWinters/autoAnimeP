from flask import Blueprint, render_template

bp = Blueprint("anime", __name__, url_prefix="/anime")

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/search")
def get_seed():
    pass

