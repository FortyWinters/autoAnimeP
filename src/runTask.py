import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
from app.lib.connect import m_DBconnector
from app.lib.logManager import m_LogManager
from app.lib.addAnimeTask import AddAnimeTask
from app.lib.addqbTask import AddqbTask
from app.lib.db_task_executor import DbTaskExecutor
from app.lib.spider_task import SpiderTask
from app.lib.spider import Mikan
from app.lib.config import m_config

logger = m_LogManager.getLogObj(sys.argv[0])
executor = ThreadPoolExecutor(max_workers=12)

spider_config = m_config.get('SPIDER')
mikan = Mikan(logger, spider_config, executor)
spider_task = SpiderTask(mikan, m_DBconnector, logger)

anime_config = m_config.get('DOWNLOAD')
qb_cinfig = m_config.get('QB')
m_addAnimeTask= AddAnimeTask(logger, executor, mikan, anime_config)
m_addqbTask = AddqbTask(qb_cinfig,logger, anime_config)
m_db_task_executor = DbTaskExecutor(logger, m_DBconnector)


def run_spider_schedule_task():
    start_time = time.time()
    spider_task.update_anime_seed()
    end_time = time.time() - start_time
    logger.info("[runTask][run_spider_schedule_task] spider_schedule_task cost time {}".format(end_time))

def run_seed_schedule_task():
    start_time = time.time()
    # 拿基础数据
    m_addAnimeTask.mikan_id_lists = m_db_task_executor.get_sub_mikan_id()
    logger.info("[runtask][run_seed_schedule_task] mikan_id_lists: {}".format(m_addAnimeTask.mikan_id_lists))

    m_addAnimeTask.mika_id_to_name_map = m_db_task_executor.create_mika_id_to_name_map(m_addAnimeTask.mikan_id_lists)
    logger.info("[runtask][run_seed_schedule_task] mikan_id to name: {}".format(m_addAnimeTask.mika_id_to_name_map))

    # 去重
    for mikan_id in m_addAnimeTask.mikan_id_lists:
        total_anime_seed_cur_mikan_id = m_db_task_executor.get_total_anime_seed_by_mikan_id(mikan_id)
        if len(total_anime_seed_cur_mikan_id) == 0:
            logger.error("[runtask][run_seed_schedule_task] failed to get anime seeds by mikan_id: {}.".format(mikan_id))
            sys.exit(0)
        
        exist_anime_task_cur_mikan_id = m_db_task_executor.get_exist_anime_task_by_mikan_id(mikan_id)
        if len(total_anime_seed_cur_mikan_id) == 0:
            logger.info("[runtask][run_seed_schedule_task] no anime tasks found by mikan_id: {}.".format(mikan_id))
            
        m_addAnimeTask.update_anime_tasks_by_mikan_id(mikan_id, 
                                       exist_anime_task_cur_mikan_id, 
                                       total_anime_seed_cur_mikan_id)
    
    logger.info("[runtask][run_seed_schedule_task] anime_task: {}".format(m_addAnimeTask.anime_task))

    # 标记使用过的seed
    for mikan_id, anime_task_cur_mikan_id in m_addAnimeTask.anime_task.items():
        if len(anime_task_cur_mikan_id) == 0:
            continue
        for eposide, torrent_name in anime_task_cur_mikan_id.items():
            m_db_task_executor.update_seed_status(torrent_name)
            logger.info("[runTask][run_seed_schedule_task] update seed: {} status to 1".format(torrent_name))

    # 下载
    for mikan_id, episode_lists_new in m_addAnimeTask.anime_task.items():
        anime_task_status_lists = m_addAnimeTask.download_anime_seed_by_mikan_id_task(mikan_id, episode_lists_new)
        # 成功列表
        if len(anime_task_status_lists['suc']) > 0:
            logger.info("[runTask][run_seed_schedule_task] Total {} new torrents of mikan_id {}, {} torrents downloaded."\
                        .format(len(episode_lists_new), mikan_id, len(anime_task_status_lists['suc'])))
            m_db_task_executor.update_torrent_status(mikan_id, anime_task_status_lists['suc'])
        
        # 失败列表
        if len(anime_task_status_lists['failed']) > 0:
            logger.info("[runTask][run_seed_schedule_task] Total {} new torrents of mikan_id {}, {} torrents fail to downloaded."\
                        .format(len(episode_lists_new), mikan_id, len(anime_task_status_lists['failed'])))

    totalTorrentInfos = m_addqbTask.getTotalTorrentInfos(m_addAnimeTask.anime_task)
    for mikan_id, torrentInfos in totalTorrentInfos.items():
        anime_name = m_addAnimeTask.mikan_id_to_name(mikan_id)
        m_addqbTask.addTorrents(anime_name, torrentInfos)

    end_time = time.time() - start_time
    logger.info("[runTask][run_seed_schedule_task] seed_schedule_task cost time {}".format(end_time))


if __name__ == '__main__':
    # m_db_task_executor.delete_anime_task_by_mikan_id(3071)
    # m_db_task_executor.delete_anime_task_by_mikan_id(3052)
    # m_db_task_executor.delete_anime_task_by_mikan_id(3060)
    # m_db_task_executor.delete_anime_task_by_mikan_id(3064)
    
    logger.info("[runtask] Begin Task at {}".format(time.time()))
    run_spider_schedule_task()
    run_seed_schedule_task()
    logger.info("[runtask] Finish Task at {}".format(time.time()))