import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from lib.connect import m_DBconnector
from lib.logManager import m_LogManager
from lib.addAnimeTask import AddAnimeTask
from lib.addqbTask import AddqbTask
from lib.db_task_executor import DbTaskExecutor
from lib.spider_task import SpiderTask
from lib.spider import Mikan
from lib.config import m_config

logger = m_LogManager.getLogObj(sys.argv[0])

conn_info = dict(
    host = "10.112.5.25",
    port = "8081",
    username = "admin",
    password = "adminadmin",
)

spider_config = m_config.get('SPIDER')
mikan = Mikan(logger, spider_config)
spider_task = SpiderTask(mikan, m_DBconnector, logger)

executor = ThreadPoolExecutor(max_workers=5)
m_addAnimeTask= AddAnimeTask(logger, executor)
m_addqbTask = AddqbTask(conn_info,logger)
m_db_task_executor = DbTaskExecutor(m_DBconnector)


def run_spider_schedule_task():
    start_time = time.time()
    spider_task.update_anime_seed()
    end_time = time.time() - start_time
    logger.info("[runTask][run_spider_schedule_task] spider_schedule_task cost time {}".format(end_time))

def run_seed_schedule_task():
    start_time = time.time()
    # 拿基础数据
    m_addAnimeTask.mikan_id_lists = m_db_task_executor.get_sub_mikan_id()
    logger.debug("[runtask] mikan_id_lists: {}".format(m_addAnimeTask.mikan_id_lists))

    m_addAnimeTask.mika_id_to_name_map = m_db_task_executor.create_mika_id_to_name_map(m_addAnimeTask.mikan_id_lists)
    logger.debug("[runtask] mikan_id_lists: {}".format(m_addAnimeTask.mika_id_to_name_map))

    # 去重
    for mikan_id in m_addAnimeTask.mikan_id_lists:
        total_anime_seed_cur_mikan_id = m_db_task_executor.get_total_anime_seed_by_mikan_id(mikan_id)
        if len(total_anime_seed_cur_mikan_id) == 0:
            logger.error("[runtask] failed to get anime seeds by mikan_id: {}.".format(mikan_id))
            sys.exit(0)
        
        exist_anime_task_cur_mikan_id = m_db_task_executor.get_exist_anime_task_by_mikan_id(mikan_id)
        if len(total_anime_seed_cur_mikan_id) == 0:
            logger.info("[runtask] no anime tasks found by mikan_id: {}.".format(mikan_id))
            
        m_addAnimeTask.update_anime_tasks_by_mikan_id(mikan_id, 
                                       exist_anime_task_cur_mikan_id, 
                                       total_anime_seed_cur_mikan_id)
    
    # 下载
    for mikan_id, episode_lists_new in m_addAnimeTask.anime_task.items():
        m_addAnimeTask.download_anime_seed_by_mikan_id_task(mikan_id, episode_lists_new)

    totalTorrentInfos = m_addqbTask.getTotalTorrentInfos(m_addAnimeTask.anime_task)
    for mikan_id, torrentInfos in totalTorrentInfos.items():
        anime_name = m_addAnimeTask.mikan_id_to_name(mikan_id)
        m_addqbTask.addTorrents(anime_name, torrentInfos)
    end_time = time.time() - start_time
    logger.info("[runTask][run_seed_schedule_task] seed_schedule_task cost time {}".format(end_time))

if __name__ == '__main__':
    # m_db_task_executor.delete_anime_task_by_mikan_id(3071)
    # m_db_task_executor.delete_anime_task_by_mikan_id(3080)
    # m_db_task_executor.delete_anime_task_by_mikan_id(3060)
    logger.info("[runtask] Begin Task at {}".format(time.time()))
    run_spider_schedule_task()
    run_seed_schedule_task()
    logger.info("[runtask] Finish Task at {}".format(time.time()))