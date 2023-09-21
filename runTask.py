import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from lib.connect import m_DBconnector
from lib.spider import m_mikan
from lib.logManager import m_LogManager
from lib.fake_add_anime_task import AddAnimeTask
from lib.addqbTask import AddqbTask
from lib.db_task_executor import DbTaskExecutor


logger = m_LogManager.getLogObj(sys.argv[0])

conn_info = dict(
    host = "10.112.5.25",
    port = "8081",
    username = "admin",
    password = "adminadmin",
)

executor = ThreadPoolExecutor(max_workers=12)
m_addAnimeTask= AddAnimeTask(logger, executor)
m_addqbTask = AddqbTask(conn_info,logger)
m_db_task_executor = DbTaskExecutor(m_DBconnector)

def run_schedule_task():
    # 拿基础数据
    m_addAnimeTask.mikan_id_lists = m_db_task_executor.get_sub_mikan_id()
    print(m_addAnimeTask.mikan_id_lists)

    m_addAnimeTask.mika_id_to_name_map = m_db_task_executor.create_mika_id_to_name_map(m_addAnimeTask.mikan_id_lists)
    print(m_addAnimeTask.mika_id_to_name_map)

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
        
    for mikan_id, anime_task_cur_mikan_id in m_addAnimeTask.anime_task.items():
        print(mikan_id, anime_task_cur_mikan_id)

    # 下载
    for mikan_id, episode_lists_new in m_addAnimeTask.anime_task.items():
        m_addAnimeTask.download_anime_seed_by_mikan_id_task(mikan_id, episode_lists_new)

    totalTorrentInfos = m_addqbTask.getTotalTorrentInfos(m_addAnimeTask.anime_task)
    for mikan_id, torrentInfos in totalTorrentInfos.items():
        anime_name = m_addAnimeTask.mikan_id_to_name(mikan_id)
        print(anime_name, torrentInfos)
        m_addqbTask.addTorrents(anime_name, torrentInfos)


if __name__ == '__main__':
    # m_db_task_executor.delete_anime_task_by_mikan_id(3071)
    # m_db_task_executor.delete_anime_task_by_mikan_id(3080)
    # m_db_task_executor.delete_anime_task_by_mikan_id(3060)
    run_schedule_task()