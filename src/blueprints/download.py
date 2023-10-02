import os
from flask import request, jsonify, render_template, Blueprint
from exts import logger, config, qb
# from lib.addqbTask import AddqbTask
from lib.connect import m_DBconnector

anime_config = config.get('DOWNLOAD')
qb_config = config.get('QB')

bp = Blueprint("download", __name__, url_prefix="/download")
# qb = AddqbTask(qb_config, logger, anime_config)

@bp.route("/", methods=['GET'])
def index():
    return render_template("download.html")

@bp.route("/get_torrent_web_info", methods=['POST'])
def get_torrent_web_info():
    mikan_id = request.args.get("mikan_id")
    episode = request.args.get("episode")
    
    if mikan_id is None:
        logger.error("[BP][get_torrent_web_info] miss mikan_id")
        return jsonify({"code": 400, "message": "failed to get torrent info", "data": None})
    if episode is None:
        logger.error("[BP][get_torrent_web_info] miss episode")
        return jsonify({"code": 400, "message": "failed to get torrent info", "data": None})

    sql = 'select torrent_name from anime_task where mikan_id={} and episode={}'.format(mikan_id, episode)
    torrent_name = m_DBconnector.execute(sql)[0][0]
    
    if torrent_name is None:
        logger.error("[BP][get_torrent_web_info] can't find torrent_name by mikan_id: {}, episode: {}".\
                     format(mikan_id, episode))
        return jsonify({"code": 400, "message": "failed to get torrent info", "data": None})
    
    torrent_web_info = qb.get_torrent_web_info(torrent_name)
    logger.info("[BP][get_torrent_web_info] get torrent_web_info: {} ".format(torrent_web_info))
    return jsonify({"code": 200, "message": "Get torrent info successfully", "data": None})