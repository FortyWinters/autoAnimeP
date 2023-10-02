import os
import time
from datetime import datetime
from flask import request, jsonify, render_template, Blueprint
from exts import mikan, logger, config, qb
from lib.models import *

bp = Blueprint("anime", __name__, url_prefix="/anime")

# 番剧列表
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
    logger.info("[BP][ANIME] index success, url: /anime/")

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    broadcast_map = dict()
    broadcast_map[2013] = [3]
    for year in range(2014, current_year):
        broadcast_map[year] = [4, 1, 2, 3]

    if current_month > 0 and current_month < 3:
        season_list = [4]
    elif current_month >= 3 and current_month < 6:
        season_list = [4, 1]
    elif current_month >= 6 and current_month < 9:
        season_list = [4, 1, 2]
    else:
        season_list = [4, 1, 2, 3]
    broadcast_map[current_year] = season_list

    return render_template("my_anime.html", anime_list=anime_order_list, broadcast_map=broadcast_map)

# 订阅番剧
@bp.route("/subscribe_anime", methods=['POST'])
def subcribe_anime():
    mikan_id = request.args.get("mikan_id")
    if not update_anime_list_subscribe_status_by_mikan_id(mikan_id, 1):
        logger.warning("[BP][ANIME] subcribe_anime, update_anime_list_subscribe_status_by_mikan_id failed, mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
        return jsonify({"code": 400, "message": "subcribe_anime", "data": None})
    
    logger.info("[BP][ANIME] subcribe_anime success, mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
    return jsonify({"code": 200, "message": "subcribe_anime", "data": None})

# 取消订阅番剧
@bp.route("/cancel_subscribe_anime", methods=['POST'])
def cancel_subscribe_anime():
    mikan_id = request.args.get("mikan_id")
    if not update_anime_list_subscribe_status_by_mikan_id(mikan_id, 0):
        logger.warning("[BP][ANIME] cancel_subcribe_anime, update_anime_list_subscribe_status_by_mikan_id failed, mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
        return jsonify({"code": 400, "message": "cancel_subscribe_anime", "data": None})
    
    logger.info("[BP][ANIME] cancel_subcribe_anime success, mikan_id: {}, subscribe_status: {}".format(mikan_id, 1))
    return jsonify({"code": 200, "message": "cancel_subscribe_anime", "data": None})

# 多线程更新种子
@bp.route("/insert_anime_seed_thread", methods=['POST'])
def insert_anime_seed_thread():
    start_time = time.time()
    mikan_id = request.args.get("mikan_id")
    update_number = 0
    fail_number = 0
    seed_set = set()
    seed_list_old = query_anime_seed_by_condition(mikan_id=mikan_id)
    for s in seed_list_old:
        seed_set.add(s["seed_url"])

    subgroup_list = mikan.get_subgroup_list(mikan_id)
    seed_list = mikan.get_seed_list_task(mikan_id, subgroup_list)

    for s in seed_list:
        if s.seed_url not in seed_set:
            if not insert_data_to_anime_seed(s.mikan_id, s.episode, s.seed_url, s.subgroup_id, s.seed_name, s.seed_status):
                fail_number += 1
                logger.warning("[BP][ANIME] insert_anime_seed_list_thread, insert_data_to_anime_seed failed, mikan_id: {}, seed_name: {}, episode: {}, subgroup_id: {}, seed_url: {}".format(mikan_id, s.seed_name, s.episode, s.subgroup_id, s.seed_url))
                continue
            update_number += 1
    logger.info("[BP][ANIME] insert_anime_seed_list_thread success, mikan_id: {}, update number: {}, fail_number: {}, time cost: {}".format(mikan_id, update_number, fail_number, time.time()-start_time))
    return jsonify({"code": 200, "message": "insert_anime_seed_thread", "data": None})

# 删除种子
@bp.route("/delete_anime_seed", methods=['POST'])
def delete_anime_seed():
    mikan_id = request.args.get("mikan_id")
    if not delete_anime_seed_by_condition(mikan_id=mikan_id):
        logger.warning("[BP][ANIME] delete_anime_seed, delete_anime_seed_by_condition failed, mikan_id: {}".format(mikan_id))
        return jsonify({"code": 400, "message": "delete_anime_seed", "data": mikan_id})

    logger.info("[BP][ANIME] delete_anime_seed success, mikan_id: {}".format(mikan_id))
    return jsonify({"code": 200, "message": "delete_anime_seed", "data": mikan_id})

# 订阅番剧下载
@bp.route("/download_subscribe_anime", methods=['POST'])
def download_subscribe_anime():
    mikan_id = request.args.get("mikan_id")
    subcribe_anime = query_anime_list_by_condition(mikan_id=mikan_id)
    anime_name = subcribe_anime[0]['anime_name']

    # anime_seed中的种子
    seed_list = query_anime_seed_by_condition(mikan_id=mikan_id, seed_status=0)
    if len(seed_list) == 0:
        logger.warning("[BP][ANIME] download_subscribe_anime failed, no seed in db, mikan_id: {}".format(mikan_id))
        return jsonify({"code": 200, "message": "download_subscribe_anime, no new seed", "data": mikan_id})

    anime_seed = dict()
    for s in seed_list:
        anime_seed[s['episode']] = s
    seed_list_unique = list(anime_seed.values())

    # anime_task中的种子
    task_list = query_anime_task_by_condition(mikan_id=mikan_id)
    task_set = set()
    for t in task_list:
        task_set.add(t['episode'])

    # 候选种子
    seed_list_update = []
    for s in seed_list_unique:
        if s['episode'] not in task_set:
            seed_list_update.append(s)

    path = "{}{}/".format(config.get('DOWNLOAD')['SEED'], mikan_id)
    if not os.path.exists(path):
        os.makedirs(path)

    # 更新种子状态
    seed_list_download = []
    for s in seed_list_update:
        if update_anime_seed_seed_status_by_seed_url(s['seed_url'], 1):
            s['path'] = path
            seed_list_download.append(s)

    # 下载种子
    seed_list_download_sucess = mikan.download_seed_task(seed_list_download)

    # 插入anime_task
    seed_list_task = []
    for s in seed_list_download_sucess:
        if insert_data_to_anime_task(s['mikan_id'], s['episode'], s['seed_url'].split('/')[3], 0):
            seed_list_task.append(s)

    # qb
    torrent_infos = dict()
    for s in seed_list_task:
        torrent_info = dict()
        torrent_name = s['seed_url'].split('/')[3]
        torrent_path = "{}{}".format(path, torrent_name)
        torrent_info['name'] = torrent_name
        torrent_info['path'] = torrent_path
        
        torrent_infos[s['episode']] = torrent_info

    qb.addTorrents(anime_name, torrent_infos)
    logger.info("[BP][ANIME] download_subscribe_anime success, mikan_id : {}, update_task_number: {}".format(mikan_id, len(seed_list_download)))
    return jsonify({"code": 200, "message": "download_subscribe_anime", "data": mikan_id})

@bp.route("/detail/<int:mikan_id>", methods=['GET'])
def detail(mikan_id):
    anime = query_anime_list_by_condition(mikan_id=mikan_id)[0]
    task_list = query_anime_task_by_condition(mikan_id=mikan_id)
    
    sorted_task_list = sorted(task_list, key=lambda x: x["episode"])
    return render_template("detail.html", anime=anime, sorted_task_list=sorted_task_list)

# 按照年份和季度更新番剧 
@bp.route("/update_anime_list", methods=['POST'])
def update_anime_list():
    year = request.args.get("year")
    season = request.args.get("season")
    
    anime_list_set = set()
    anime_list_old = query_anime_list_by_condition()
    for a in anime_list_old:
        anime_list_set.add(a["mikan_id"])

    anime_broadcast_set = set()
    anime_broadcast_old = query_anime_broadcast_by_condition(year=year, season=season)
    for a in anime_broadcast_old:
        anime_broadcast_set.add(a["mikan_id"])

    anime_list_new = mikan.get_anime_list_by_conditon(int(year), int(season))
    anime_list_update = []
    for a in anime_list_new:
        if a.mikan_id not in anime_broadcast_set:
            anime_list_update.append(a)
    
    img_path = config.get('DOWNLOAD')['IMG']
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    
    update_number = 0
    fail_number = 0
    img_list = []
    for a in anime_list_update:
        img_info = {}
        if not insert_data_to_anime_broadcast(a.mikan_id, year, season):
            logger.warning("[BP][ANIME] update_anime_list error, insert_data_to_anime_broadcast failed, mikan_id: {}, year: {}, season: {}".format(a.mikan_id, year, season))
            fail_number += 1
            continue
        else:
            if a.mikan_id not in anime_list_set:
                if not insert_data_to_anime_list(a.mikan_id, a.anime_name, a.img_url, a.update_day, a.anime_type, a.subscribe_status):
                    logger.warning("[BP][ANIME] update_anime_list error, insert_data_to_anime_list failed, mikan_id: {}".format(a.mikan_id))
                    fail_number += 1
                    continue
                img_info['mikan_id'] = a.mikan_id
                img_info['img_url'] = a.img_url
                img_info['path'] = img_path
                img_list.append(img_info)
                update_number += 1

    img_list_download = mikan.download_img_task(img_list)
    
    img_set = {tuple(d.items()) for d in img_list}
    img_set_download = {tuple(d.items()) for d in img_list_download}
    img_set_download_failed = img_set - img_set_download

    for img in img_set_download_failed:
        logger.warning("[BP][ANIME] update_anime_list, mikan.download_img failed, mikan_id: {}, img_url: {}, img_path: {}".format(img['mikan_id'], img['img_url'], img['path']))

    logger.info("[BP][ANIME] update_anime_list success, update number: {}, fail number: {}".format(update_number, fail_number))
    return jsonify({"code": 200, "message": "update_anime_list", "data": None})

# 按照年份和季度查看番剧列表
@bp.route("/<int:url_year>/<int:url_season>", methods=['GET'])
def anime_list_by_broadcast(url_year, url_season):
    broadcast_list = query_anime_broadcast_by_condition(year=url_year, season=url_season)
    anime_list = []
    for b in broadcast_list:
        anime = query_anime_list_by_condition(mikan_id=b["mikan_id"])[0]
        anime_list.append(anime)
    
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

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    broadcast_map = dict()
    broadcast_map[2013] = [3]
    for year in range(2014, current_year):
        broadcast_map[year] = [4, 1, 2, 3]

    if current_month > 0 and current_month < 3:
        season_list = [4]
    elif current_month >= 3 and current_month < 6:
        season_list = [4, 1]
    elif current_month >= 6 and current_month < 9:
        season_list = [4, 1, 2]
    else:
        season_list = [4, 1, 2, 3]
    broadcast_map[current_year] = season_list

    logger.info("[BP][ANIME] anime_list_by_broadcast success, url: /anime/")
    return render_template("anime.html", anime_list=anime_order_list, broadcast_map=broadcast_map, url_year=url_year, url_season=url_season)