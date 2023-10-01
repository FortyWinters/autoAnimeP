import os
from flask import request, jsonify, render_template, Blueprint
from exts import logger

bp = Blueprint("setting", __name__, url_prefix="/setting")

@bp.route("/", methods=['GET'])
def index():
    return render_template("setting.html")

@bp.route("/start_main_task", methods=['POST'])
def start_main_task():
    import os
    import multiprocessing
    from flask import jsonify

    if os.path.exists('config_file/daemon_pid.txt'):
        with open('config_file/daemon_pid.txt', 'r') as file:
            pid = int(file.read())
        logger.info("[BP][start_main_task] daemon process has been started with pid: {} .".format(pid))
        return jsonify({"code": 200, "message": "daemon process has been started", "data": None})
    
    interval = request.args.get("interval")
    if interval is None:
        interval = 2
        logger.warning("[BP][start_main_task] failed to get interval, set interval to default: {} .".format(interval))
    else:
        logger.info("[BP][start_main_task] set interval to: {} .".format(interval))

    daemon = multiprocessing.Process(target=start_fn,args=(int(interval),))
    daemon.daemon = True
    daemon.start()
    
    daemon_pid = daemon.pid
    with open('config_file/daemon_pid.txt', 'w') as file:
        file.write(str(daemon_pid))
    logger.info("[BP][start_main_task] strat new daemon process with pid  {} .".format(daemon_pid))
    return jsonify({"code": 200, "message": "stop_main_task", "data": None})

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
    import os
    import signal
    import multiprocessing
    from flask import jsonify
    
    if os.path.exists('config_file/daemon_pid.txt'):
        with open('config_file/daemon_pid.txt', 'r') as file:
            pid = int(file.read())
        try:
            os.kill(pid, signal.SIGTERM)
            logger.info("[BP][change_main_task_interval] successfully shut down daemon with pid: {} .".format(pid))
        except Exception as e:
            logger.error("[BP][change_main_task_interval] failed to shut down daemon with pid: {} .".format(pid))
    else:
        logger.warning("[BP][change_main_task_interval] daemon process not started ")

    interval = request.args.get("interval")
    if interval is None:
        interval = 2
        logger.warning("[BP][change_main_task_interval] failed to get interval, set interval to default: {} .".format(interval))
    else:
        logger.info("[BP][change_main_task_interval] set interval to: {} .".format(interval))
    
    daemon = multiprocessing.Process(target=start_fn,args=(int(interval),))
    daemon.daemon = True
    daemon.start()
    
    daemon_pid = daemon.pid
    with open('config_file/daemon_pid.txt', 'w') as file:
        file.write(str(daemon_pid))
    logger.info("[BP][change_main_task_interval] strat new daemon process with pid {} .".format(daemon_pid))
    return jsonify({"code": 200, "message": "change_main_task_interval", "data": None})

def start_fn(interval):
    from lib.config import m_config
    from lib.connect import m_DBconnector
    from lib.spider import Mikan
    from concurrent.futures import ThreadPoolExecutor
    from lib.do_anime_task import doTask

    anime_config = m_config.get('DOWNLOAD')
    qb_config = m_config.get('QB')
    spider_config = m_config.get('SPIDER')

    executor = ThreadPoolExecutor(max_workers=12)
    mikan = Mikan(logger, spider_config, executor)
    m_doTask = doTask(logger, mikan, anime_config, qb_config, m_DBconnector, executor)

    logger.info('Running daemon process')
    m_doTask.execAllTask(interval)