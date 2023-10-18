import os
import subprocess
import signal
import multiprocessing
from flask import request, jsonify, render_template, Blueprint
from exts import logger, broadcast_map
from lib.config import m_config
from lib.connect import m_DBconnector
from lib.spider import Mikan
from concurrent.futures import ThreadPoolExecutor
from lib.do_anime_task import doTask

bp = Blueprint("setting", __name__, url_prefix="/setting")
anime_config = m_config.get('DOWNLOAD')
qb_config = m_config.get('QB')
spider_config = m_config.get('SPIDER')

executor = ThreadPoolExecutor(max_workers=12)
mikan = Mikan(logger, spider_config, executor)
m_doTask = doTask(logger, mikan, anime_config, qb_config, m_DBconnector, executor)

@bp.route("/", methods=['GET'])
def index():
    if os.path.exists('config_file/daemon_pid.txt'):
        with open('config_file/daemon_pid.txt', 'r') as file:
            pid = file.read()
        if not is_process_running(pid):
            os.remove('config_file/daemon_pid.txt')
    return render_template("setting.html", broadcast_map=broadcast_map)

def is_process_running(pid):
    cmd = f'ps -p {pid}'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    output = result.stdout.decode()
    print(output)
    return pid in output

@bp.route("/start_main_task", methods=['POST'])
def start_main_task():
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

@bp.route("/get_daemon_pid", methods=['GET'])
def get_daemon_pid():
    try:
        with open('config_file/daemon_pid.txt', 'r') as file:
            pid = int(file.read())
    except FileNotFoundError:
        pid = None

    logger.info("[BP][DOWNLOAD] get_daemon_pid success, pid: {}".format(pid))
    return jsonify({"code": 200, "message": "get_daemon_pid", "data": pid})

@bp.route("/load_fin_task", methods=['GET'])
def load_fin_task():
    m_doTask.load_fin_task()
    return jsonify({"code": 200, "message": "load_fin_task", "data": None})

# global filter
@bp.route("/add_global_episode_offset_filter", methods=['POST'])
def add_global_episode_offset_filter():
    episode_offset = request.args.get("episode_offset")
    m_doTask.add_global_episode_offset_filter(episode_offset)
    return jsonify({"code": 200, "message": "add_global_episode_offset_filter", "data": None})

@bp.route("/add_global_skip_subgroup_filter_filter", methods=['POST'])
def add_global_skip_subgroup_filter_filter():
    skip_subgroup = request.args.get("skip_subgroup")
    m_doTask.add_global_skip_subgroup_filter_filter(skip_subgroup)
    return jsonify({"code": 200, "message": "add_global_skip_subgroup_filter_filter", "data": None})

@bp.route("/del_global_episode_offset_filter", methods=['GET'])
def del_global_episode_offset_filter():
    m_doTask.del_global_episode_offset_filter()
    return jsonify({"code": 200, "message": "del_global_episode_offset_filter", "data": None})

@bp.route("/del_global_skip_subgroup_filter", methods=['GET'])
def del_global_skip_subgroup_filter():
    m_doTask.del_global_skip_subgroup_filter()
    return jsonify({"code": 200, "message": "del_global_skip_subgroup_filter", "data": None})

@bp.route("/del_global_skip_subgroup_filter_by_skip_subgroup", methods=['POST'])
def del_global_skip_subgroup_filter_by_skip_subgroup():
    skip_subgroup = request.args.get("skip_subgroup")
    m_doTask.del_global_skip_subgroup_filter_by_skip_subgroup(skip_subgroup)
    return jsonify({"code": 200, "message": "del_global_skip_subgroup_filter_by_skip_subgroup", "data": None})

@bp.route("/get_global_episode_offset_filter", methods=['GET'])
def get_global_episode_offset_filter():
    episode_offset = m_doTask.get_global_episode_offset_filter()
    return jsonify({"code": 200, "message": "get_global_episode_offset_filter", "data": episode_offset})

@bp.route("/get_global_skip_subgroup_filter", methods=['GET'])
def get_global_skip_subgroup_filter():
    skip_subgroup_list = m_doTask.get_global_skip_subgroup_filter()
    return jsonify({"code": 200, "message": "get_global_skip_subgroup_filter", "data": skip_subgroup_list})

# local filter
@bp.route("/add_episode_offset_filter_by_mikan_id", methods=['POST'])
def add_episode_offset_filter_by_mikan_id():
    mikan_id = request.args.get("mikan_id")
    episode_offset = request.args.get("episode_offset")
    m_doTask.add_episode_offset_filter_by_mikan_id(mikan_id, episode_offset)
    return jsonify({"code": 200, "message": "add_episode_offset_filter_by_mikan_id", "data": None})

@bp.route("/add_skip_subgroup_filter_by_mikan_id", methods=['POST'])
def add_skip_subgroup_filter_by_mikan_id():
    mikan_id = request.args.get("mikan_id")
    skip_subgroup = request.args.get("skip_subgroup")
    m_doTask.add_skip_subgroup_filter_by_mikan_id(mikan_id, skip_subgroup)
    return jsonify({"code": 200, "message": "add_skip_subgroup_filter_by_mikan_id", "data": None})

@bp.route("/del_episode_offset_filter_by_mikan_id", methods=['POST'])
def del_episode_offset_filter_by_mikan_id():
    mikan_id = request.args.get("mikan_id")
    m_doTask.del_episode_offset_filter_by_mikan_id(mikan_id)
    return jsonify({"code": 200, "message": "del_episode_offset_filter_by_mikan_id", "data": None})

@bp.route("/del_skip_subgroup_filter_by_mikan_id", methods=['POST'])
def del_skip_subgroup_filter_by_mikan_id():
    mikan_id = request.args.get("mikan_id")
    m_doTask.del_skip_subgroup_filter_by_mikan_id(mikan_id)
    return jsonify({"code": 200, "message": "del_skip_subgroup_filter_by_mikan_id", "data": None})

@bp.route("/del_skip_subgroup_filter_by_mikan_id_and_skip_subgroup", methods=['POST'])
def del_skip_subgroup_filter_by_mikan_id_and_skip_subgroup():
    mikan_id = request.args.get("mikan_id")
    skip_subgroup = request.args.get("skip_subgroup")
    m_doTask.del_skip_subgroup_filter_by_mikan_id_and_skip_subgroup(mikan_id, skip_subgroup)
    return jsonify({"code": 200, "message": "del_skip_subgroup_filter_by_mikan_id_and_skip_subgroup", "data": None})

@bp.route("/get_episode_offset_filter_by_mikan_id", methods=['POST'])
def get_episode_offset_filter_by_mikan_id():
    mikan_id = request.args.get("mikan_id")
    episode_offset = m_doTask.get_episode_offset_filter_by_mikan_id(mikan_id)
    return jsonify({"code": 200, "message": "get_episode_offset_filter_by_mikan_id", "data": episode_offset})

@bp.route("/get_skip_subgroup_filter_by_mikan_id", methods=['POST'])
def get_skip_subgroup_filter_by_mikan_id():
    mikan_id = request.args.get("mikan_id")
    skip_subgroup = m_doTask.get_skip_subgroup_filter_by_mikan_id(mikan_id)
    return jsonify({"code": 200, "message": "get_skip_subgroup_filter_by_mikan_id", "data": skip_subgroup})