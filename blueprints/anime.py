from flask import Blueprint, render_template
from exts import mikan, logger
from models import *

bp = Blueprint("anime", __name__, url_prefix="/anime")

@bp.route("/")
def index():
    anime_list = query_list_by_anime_name()
    return render_template("anime_list.html", anime_list=anime_list)

@bp.route("/update_anime_list")
def update_anime_list():
    img_path = "static/img/anime_list/"
    update_number = 0
    fail_number = 0

    anime_set = set()
    anime_list_old = query_list_by_anime_name()
    for a in anime_list_old:
        anime_set.add(a["mikan_id"])

    #mikan = Mikan()
    anime_list_new = mikan.get_anime_list()
    for a in anime_list_new:
        if a.mikan_id not in anime_set:
            insert_res = insert_data_to_anime_list(a.anime_name, a.mikan_id, a.img_url, a.update_day, a.anime_type, a.subscribe_status)
            if not insert_res:
                fail_number += 1
                logger.warning("[BP][ANIME]update_anime_list error, insert_data_to_anime_list failed, " +
                    "mikan_id: {}".format(a.mikan_id))
                # print("[ERROR][BP][ANIME]update_anime_list error, insert_data_to_anime_list failed, " +
                #   "mikan_id: {}".format(a.mikan_id)) 
                continue
            update_number += 1
            
            img_res = mikan.download_img(a.img_url, img_path)
            if not img_res:
                logger.warning("[ERROR][BP][ANIME]update_anime_list error, mikan.download_img failed, " +
                    "mikan_id: {}, img_url: {}, img_path: {}".format(a.mikan_id, a.img_url, img_path))
                # print("[ERROR][BP][ANIME]update_anime_list error, mikan.download_img failed, " +
                #   "mikan_id: {}, img_url: {}, img_path: {}".format(a.mikan_id, a.img_url, img_path))
    logger.info("[BP][ANIME]update_anime_list, updating anime finished, " + 
          "update number: {}, fail number: {}".format(update_number, fail_number))        
    # print("[INFO][BP][ANIME]update_anime_list, updating anime finished, " + 
    #       "update number: {}, fail number: {}".format(update_number, fail_number))
    return render_template("anime_list.html")

@bp.route("/subscribe_anime/<int:mikan_id>")
def subcribe_anime(mikan_id):
    if not update_list_subscribe_status(mikan_id, 1):
        # print("[ERROR][BP][ANIME]subcribe_anime error, update_anime_subscribe_status failed, " +
            #  "mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
        logger.warning("[BP][ANIME]subcribe_anime error, update_anime_subscribe_status failed, " +
              "mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))      
    return render_template("anime_list.html")
    

    
@bp.route("/cancle_subscribe_anime/<int:mikan_id>")
def cancle_subscribe_anime(mikan_id):
    if not update_list_subscribe_status(mikan_id, 0):
        # print("[ERROR][BP][ANIME]cancle_subscribe_anime error, update_anime_subscribe_status failed, " +
            #  "mikan_id: {}, subscribe_status: {}".format(mikan_id, 0))
        logger.warning("[BP][ANIME]cancel_subcribe_anime error, update_anime_subscribe_status failed, " +
            "mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))    
    return render_template("anime_list.html")


    

    

    

@bp.route("/insert_anime_seed_list/<int:mikan_id>")
def insert_anime_seed_list(mikan_id):
    update_number = 0
    fail_number = 0

    seed_set = set()
    seed_list_old = query_seed_by_anime_name(mikan_id=mikan_id)
    for s in seed_list_old:
        seed_set.add(s["seed_url"])

    # mikan = Mikan()
    subgroup_list = mikan.get_subgroup_list(mikan_id)
    for sub in subgroup_list:
        seed_list = mikan.get_seed_list(mikan_id, sub.subgroup_id)
        for s in seed_list:
            if s.seed_url not in seed_set:
                res_insert = insert_data_to_anime_seed(s.mikan_id, s.episode, s.seed_url, s.subgroup_id, s.seed_name)
                if not res_insert:
                    fail_number += 1
                    # print("[ERROR][BP][ANIME]insert_anime_seed_list error, insert_data_to_anime_seed failed, " +
                    #       "mikan_id: {}, seed_name: {}, episode: {}, subgroup_id: {}, seed_url: {}".format(
                    #           mikan_id, s.seed_name, s.episode, s.subgroup_id, s.seed_url))
                    logger.warning("[BP][ANIME]insert_anime_seed_list error, insert_data_to_anime_seed failed, " +
                          "mikan_id: {}, seed_name: {}, episode: {}, subgroup_id: {}, seed_url: {}".format(
                              mikan_id, s.seed_name, s.episode, s.subgroup_id, s.seed_url))
                    continue
                update_number += 1
    # print("[INFO][BP][ANIME]insert_anime_seed_list, inserting anime seed finished, " + 
    #     "mikan_id: {}, update number: {}, fail_number: {}".format(mikan_id, update_number, fail_number))
    logger.info("[BP][ANIME]insert_anime_seed_list, inserting anime seed finished, " + 
        "mikan_id: {}, update number: {}, fail_number: {}".format(mikan_id, update_number, fail_number))