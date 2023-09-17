from flask import Blueprint, render_template
from exts import mikan, logger
from lib.models import *
from flask import request, jsonify

bp = Blueprint("anime", __name__, url_prefix="/anime")

# 渲染番剧列表
@bp.route("/")
def index():
    anime_list = query_anime_list_by_condition()
    subscribe_list = []
    unsubscribe_list = []
    anime_order_list = []
    for a in anime_list:
        if a['subscribe_status'] == 1:
            subscribe_list.append(a)
        else:
            unsubscribe_list.append(a)
    
    subscribe_order_list = sorted(subscribe_list, key=lambda x: x['update_day'])
    unsubscribe_order_list = sorted(unsubscribe_list, key=lambda x: x['update_day'])
    for a in subscribe_order_list:
        anime_order_list.append(a)
    for a in unsubscribe_order_list:
        anime_order_list.append(a)

    return render_template("anime_list.html", anime_list=anime_order_list)

# 更新番剧列表
@bp.route("/update_anime_list", methods=['GET'])
def update_anime_list():
    img_path = "static/img/anime_list/"
    update_number = 0
    fail_number = 0
    anime_set = set()
    anime_list_old = query_anime_list_by_condition()
    for a in anime_list_old:
        anime_set.add(a["mikan_id"])

    anime_list_new = mikan.get_anime_list()
    for a in anime_list_new:
        if a.mikan_id not in anime_set:
            if not insert_data_to_anime_list(a.mikan_id, a.anime_name, a.img_url, a.update_day, a.anime_type, a.subscribe_status):
                fail_number += 1
                logger.warning("[BP][ANIME]update_anime_list error, insert_data_to_anime_list failed, mikan_id: {}".format(a.mikan_id))
                continue
            update_number += 1

            if not mikan.download_img(a.img_url, img_path):
                logger.warning("[ERROR][BP][ANIME]update_anime_list error, mikan.download_img failed, mikan_id: {}, img_url: {}, img_path: {}".format(a.mikan_id, a.img_url, img_path))
                return jsonify({"code": 400, "message": "update_anime_list", "data": None})
    logger.info("[BP][ANIME]update_anime_list, updating anime finished, update number: {}, fail number: {}".format(update_number, fail_number))
    return jsonify({"code": 200, "message": "update_anime_list", "data": None})

# 订阅番剧
@bp.route("/subscribe_anime", methods=['POST'])
def subcribe_anime():
    mikan_id = request.args.get("mikan_id")
    if not update_anime_list_subscribe_status_by_mikan_id(mikan_id, 1):
        logger.warning("[BP][ANIME]subcribe_anime error, update_anime_subscribe_status failed, mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
        return jsonify({"code": 400, "message": "subcribe_anime", "data": None})
    
    logger.info("[BP][ANIME]subcribe_anime success, mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
    return jsonify({"code": 200, "message": "subcribe_anime", "data": None})

# 取消订阅番剧
@bp.route("/cancel_subscribe_anime", methods=['POST'])
def cancel_subscribe_anime():
    mikan_id = request.args.get("mikan_id")
    if not update_anime_list_subscribe_status_by_mikan_id(mikan_id, 0):
        logger.warning("[BP][ANIME]cancel_subcribe_anime error, update_anime_subscribe_status failed, mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
        return jsonify({"code": 400, "message": "cancel_subscribe_anime", "data": None})
    
    logger.info("[BP][ANIME]cancel_subcribe_anime success, mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
    return jsonify({"code": 200, "message": "cancel_subscribe_anime", "data": None})

# 更新种子
@bp.route("/insert_anime_seed", methods=['POST'])
def insert_anime_seed():
    mikan_id = request.args.get("mikan_id")
    update_number = 0
    fail_number = 0
    seed_set = set()
    seed_list_old = query_anime_seed_by_condition(mikan_id=mikan_id)
    for s in seed_list_old:
        seed_set.add(s["seed_url"])

    subgroup_list = mikan.get_subgroup_list(mikan_id)
    for sub in subgroup_list:
        seed_list = mikan.get_seed_list(mikan_id, sub.subgroup_id)
        for s in seed_list:
            if s.seed_url not in seed_set:
                if not insert_data_to_anime_seed(s.mikan_id, s.episode, s.seed_url, s.subgroup_id, s.seed_name):
                    fail_number += 1
                    logger.warning("[BP][ANIME]insert_anime_seed_list error, insert_data_to_anime_seed failed, mikan_id: {}, seed_name: {}, episode: {}, subgroup_id: {}, seed_url: {}".format(mikan_id, s.seed_name, s.episode, s.subgroup_id, s.seed_url))
                    continue
                update_number += 1
    logger.info("[BP][ANIME]insert_anime_seed_list, inserting anime seed finished, mikan_id: {}, update number: {}, fail_number: {}".format(mikan_id, update_number, fail_number))
    return jsonify({"code": 200, "message": "insert_anime_seed", "data": None})

# 删除种子
@bp.route("/delete_anime_seed", methods=['POST'])
def delete_anime_seed():
    mikan_id = request.args.get("mikan_id")
    if not delete_anime_seed_by_condition(mikan_id=mikan_id):
        logger.warning("[BP][ANIME]delete_anime_seed failed, mikan_id: {}".format(mikan_id))
        return jsonify({"code": 400, "message": "delete_anime_seed", "data": mikan_id})

    logger.info("[BP][ANIME]delete_anime_seed finished, mikan_id: {}".format(mikan_id))
    return jsonify({"code": 200, "message": "delete_anime_seed", "data": mikan_id})

# # 测试插入方法insert_data_to_anime_list_new的默认参数
# @bp.route("/test1")
# def test1():
#     result = insert_data_to_anime_list_new(mikan_id=683)
#     if result:
#         return "Yes"
#     else:
#         return "NO"


# # 测试条件删除
# @bp.route("/test2")
# def test2():
#     result = delete_anime_list_by_condition(update_day=0)
#     if result:
#         return "Yes"
#     else:
#         return "No"


# # 测试条件查询
# @bp.route("/test3")
# def test3():
#     result = query_list_by_anime_name_new(subscribe_status=0, update_day=3)
#     return result
