import os
from flask import request, jsonify, render_template, Blueprint
from exts import logger, config, qb
# from lib.addqbTask import AddqbTask
from lib.connect import m_DBconnector
from lib.models import *

anime_config = config.get('DOWNLOAD')
qb_config = config.get('QB')

bp = Blueprint("download", __name__, url_prefix="/download")
# qb = AddqbTask(qb_config, logger, anime_config)


@bp.route("/", methods=['GET'])
def index():
    return render_template("download.html")

@bp.route("/get", methods=['GET'])
def get():
    torrent_web_info_list = []
    task_list = query_anime_task_by_condition(qb_task_status=0)
    for task in task_list:
        mikan_id = task['mikan_id']
        episode = task['episode']
        torrent_web_info = get_torrent_web_info(mikan_id, episode)
        torrent_web_info_list.append(torrent_web_info)
    return jsonify({"code": 200, "message": "subcribe_anime", "data": torrent_web_info_list})

def get_torrent_web_info(mikan_id, episode):   
    sql = 'select torrent_name from anime_task where mikan_id={} and episode={}'.format(mikan_id, episode)
    torrent_name = m_DBconnector.execute(sql)

    if len(torrent_name) == 0:
        logger.warning("[BP][get_torrent_web_info] can't find torrent_name by mikan_id: {}, episode: {}".\
                     format(mikan_id, episode))
    
    torrent_name = torrent_name[0][0]
    print(torrent_name)
    torrent_web_info = qb.get_torrent_web_info(torrent_name)
    logger.info("[BP][get_torrent_web_info] get torrent_web_info: {} ".format(torrent_web_info))
    return torrent_web_info

@bp.route("/delete_task", methods=['POST'])
def delete_task():
    mikan_id = request.args.get("mikan_id")
    episode = request.args.get("episode")

    if mikan_id is None:
        logger.error("[BP][get_torrent_web_info] miss mikan_id")
        return jsonify({"code": 400, "message": "failed to get torrent info, missing mikan_id", "data": None})
    if episode is None:
        logger.error("[BP][get_torrent_web_info] miss episode")
        return jsonify({"code": 400, "message": "failed to get torrent info, missing episode", "data": None})
    
    sql = 'select torrent_name from anime_task where mikan_id={} and episode={}'.format(mikan_id, episode)
    torrent_name = m_DBconnector.execute(sql)

    if len(torrent_name) == 0:
        logger.warning("[BP][get_torrent_web_info] can't find torrent_name by mikan_id: {}, episode: {}".\
                     format(mikan_id, episode))
        return jsonify({"code": 400, "message": "torrent is not exist", "data": None})
    
    torrent_name = torrent_name[0][0]
    qb.del_torrent(torrent_name)

    sql = 'DELETE FROM anime_task WHERE torrent_name="{}"'.format(torrent_name)
    m_DBconnector.execute(sql)
    return jsonify({"code": 200, "message": "delet torrent successfully", "data": None})