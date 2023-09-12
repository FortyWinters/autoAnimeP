from flask import Blueprint, render_template
from spider import Mikan
from models import *

bp = Blueprint("anime", __name__, url_prefix="/anime")

@bp.route("/")
def index():
    # mikan = Mikan()
    # anime_list = mikan.get_anime_list()
    # anime_name = []
    query_list_by_anime_name()


    # for a in anime_list:
    #     anime_name.append(a.anime_name)
    # return render_template("anime_list.html", anime_name=anime_name)
    return render_template("anime_list.html")


