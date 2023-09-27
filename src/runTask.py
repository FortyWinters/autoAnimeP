import sys
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from app.lib.connect import m_DBconnector
from app.lib.logManager import m_LogManager
from app.lib.config import m_config
from app.lib.spider_task import SpiderTask
from app.lib.spider import Mikan
from app.lib.do_anime_task import doAnimeTask

logger = m_LogManager.getLogObj(sys.argv[0])
executor = ThreadPoolExecutor(max_workers=12)

spider_config = m_config.get('SPIDER')
mikan = Mikan(logger, spider_config, executor)
spider_task = SpiderTask(mikan, m_DBconnector, logger)

anime_config = m_config.get('DOWNLOAD')
qb_cinfig = m_config.get('QB')
m_doAnimeTask = doAnimeTask(logger, mikan, anime_config, qb_cinfig, m_DBconnector, executor)

def run_spider_schedule_task():
    start_time = time.time()
    spider_task.update_anime_seed()
    end_time = time.time() - start_time
    logger.info("[runTask][run_spider_schedule_task] spider_schedule_task cost time {}".format(end_time))

def run_seed_schedule_task():
    start_time = time.time()
    m_doAnimeTask.seed_schedule_task()
    end_time = time.time() - start_time
    logger.info("[runTask][run_spider_schedule_task] spider_schedule_task cost time {}".format(end_time))


if __name__ == '__main__':
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("[runtask] Begin Task at {}".format(start_time))
    run_spider_schedule_task()
    run_seed_schedule_task()
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("[runtask] Finish Task at {}".format(end_time))