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

@bp.route("/insert_anime_list")
def insert_anime_list():
    mikan = Mikan()
    anime_list = mikan.get_anime_list()
    for a in anime_list:
        img_name = a.img_url.split('/')[4]
        insert_data_to_anime_list(a.anime_name, a.mikan_id, img_name, a.update_day)
    print("anime list insert finished")