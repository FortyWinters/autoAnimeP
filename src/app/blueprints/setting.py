import os
import time
from flask import request, jsonify, render_template, Blueprint
from exts import mikan, logger, config, qb, executor
from lib.models import *

bp = Blueprint("setting", __name__, url_prefix="/setting")

@bp.route("/start_main_task", methods=['POST'])
def start_main_task():
    from lib.connect import m_DBconnector
    from lib.do_anime_task import doTask

    interval = request.args.get("interval")
    if interval is None:
        interval = 2
        logger.warning("[BP][start_main_task] failed to get interval, set interval to default: {} .".format(interval))
    else:
        logger.warning("[BP][start_main_task] set interval to: {} .".format(interval))

    if os.path.exists('config_file/daemon_pid.txt'):
        with open('config_file/daemon_pid.txt', 'r') as file:
            pid = int(file.read())
        logger.info("[BP][start_main_task] daemon process has been started with pid: {} .".format(pid))
        return jsonify({"code": 200, "message": "daemon process has been started", "data": None})
    
    anime_config = config.get('DOWNLOAD')
    qb_cinfig = config.get('QB')
    m_doTask = doTask(logger, mikan, anime_config, qb_cinfig, m_DBconnector, executor)

    pid = os.fork()
    if pid > 0:
        with open('config_file/daemon_pid.txt', 'w') as file:
            file.write(str(pid))
        logger.info("[BP][start_main_task] daemon process id is {} .".format(pid))
        return jsonify({"code": 200, "message": "start_main_task", "data": None})
    m_doTask.execAllTask(interval)

@bp.route("/stop_main_task", methods=['POST'])
def stop_main_task():
    import signal

    if not os.path.exists('config_file/daemon_pid.txt'):
        logger.error("[BP][stop_main_task] daemon process not started")
        return jsonify({"code": 200, "message": "daemon process not started", "data": None})

    with open('config_file/daemon_pid.txt', 'r') as file:
        pid = int(file.read())
    logger.info("[BP][stop_main_task] m_pid is {}.".format(pid))
    
    try:
        os.kill(pid, signal.SIGTERM)
        logger.info("[BP][stop_main_task] successfully shut down daemon with pid: {} .".format(pid))
    except Exception as e:
        logger.error("[BP][stop_main_task] failed to shut down daemon with pid: {} .".format(pid))

    os.remove('config_file/daemon_pid.txt')
    return jsonify({"code": 200, "message": "stop_main_task", "data": None})

@bp.route("/change_main_task_interval", methods=['POST'])
def change_main_task_interval():
    import signal
    from lib.connect import m_DBconnector
    from lib.do_anime_task import doTask
    
    if os.path.exists('config_file/daemon_pid.txt'):
        with open('config_file/daemon_pid.txt', 'r') as file:
            pid = int(file.read())
        try:
            os.kill(pid, signal.SIGTERM)
            logger.info("[BP][stop_main_task] successfully shut down daemon with pid: {} .".format(pid))
        except Exception as e:
            logger.error("[BP][stop_main_task] failed to shut down daemon with pid: {} .".format(pid))
    
    interval = request.args.get("interval")
    if interval is None:
        interval = 2
        logger.warning("[BP][start_main_task] failed to get interval, set interval to default: {} .".format(interval))
    else:
        logger.warning("[BP][start_main_task] set interval to: {} .".format(interval))
    
    anime_config = config.get('DOWNLOAD')
    qb_cinfig = config.get('QB')
    m_doTask = doTask(logger, mikan, anime_config, qb_cinfig, m_DBconnector, executor)

    pid = os.fork()
    if pid > 0:
        with open('config_file/daemon_pid.txt', 'w') as file:
            file.write(str(pid))
        logger.info("[BP][change_main_task_interval] new daemon process id is {} .".format(pid))
        return jsonify({"code": 200, "message": "change_main_task_interval", "data": None})
    m_doTask.execAllTask(interval)

