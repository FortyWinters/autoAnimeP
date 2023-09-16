from flask import Blueprint, render_template
from lib.spider import Mikan

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/")
def index():
    return render_template("index.html")