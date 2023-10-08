import sys
import time
import datetime
import schedule
from .addAnimeTask import AddAnimeTask
from .addqbTask import AddqbTask
from .db_task_executor import DbTaskExecutor
from .spider_task import SpiderTask

class doAnimeTask(AddAnimeTask, AddqbTask, DbTaskExecutor):
    def __init__(self, logger, mikan, anime_config, qb_cinfig, m_DBconnector, executor):
        AddAnimeTask.__init__(self, logger, executor, mikan, anime_config)
        AddqbTask.__init__(self, qb_cinfig, logger, anime_config)
        DbTaskExecutor.__init__(self, logger, m_DBconnector)
        self.logger = logger

    def seed_schedule_task(self):
        start_time = time.time()
        # 拿基础数据
        self.mikan_id_lists = self.get_sub_mikan_id()
        self.logger.info("[do_anime_task][doAnimeTask][seed_schedule_task] mikan_id_lists: {}".format(self.mikan_id_lists))

        self.mika_id_to_name_map = self.create_mika_id_to_name_map(self.mikan_id_lists)
        self.logger.info("[do_anime_task][doAnimeTask][seed_schedule_task] mikan_id to name: {}".format(self.mika_id_to_name_map))

        # 去重
        for mikan_id in self.mikan_id_lists:
            total_anime_seed_cur_mikan_id = self.get_total_anime_seed_by_mikan_id(mikan_id)
            if len(total_anime_seed_cur_mikan_id) == 0:
                self.logger.error("[do_anime_task][doAnimeTask][seed_schedule_task] failed to get anime seeds by mikan_id: {}.".format(mikan_id))
                sys.exit(0)
            
            exist_anime_task_cur_mikan_id = self.get_exist_anime_task_by_mikan_id(mikan_id)
            if len(total_anime_seed_cur_mikan_id) == 0:
                self.logger.info("[do_anime_task][doAnimeTask][seed_schedule_task] no anime tasks found by mikan_id: {}.".format(mikan_id))
            
            # Get animeTask, animeTask : {mikan_id, {episode, [torrent_name, subgroupname]]}}
            self.update_anime_tasks_by_mikan_id(mikan_id, 
                                                exist_anime_task_cur_mikan_id, 
                                                total_anime_seed_cur_mikan_id)
        
        self.logger.info("[do_anime_task][doAnimeTask][seed_schedule_task] anime_task: {}".format(self.anime_task))

        # 标记使用过的seed
        for mikan_id, anime_task_cur_mikan_id in self.anime_task.items():
            if len(anime_task_cur_mikan_id) == 0:
                continue
            for eposide, torrent_info in anime_task_cur_mikan_id.items():
                self.update_seed_status(torrent_info[0])
                self.logger.info("[do_anime_task][doAnimeTask][seed_schedule_task] update seed: {} status to 1".format(torrent_info[0]))

        # 下载
        for mikan_id, episode_lists_new in self.anime_task.items():
            anime_task_status_lists = self.download_anime_seed_by_mikan_id_task(mikan_id, episode_lists_new)
            # 成功列表
            if len(anime_task_status_lists['suc']) > 0:
                self.logger.info("[do_anime_task][doAnimeTask][seed_schedule_task] Total {} new torrents of mikan_id {}, {} torrents downloaded."\
                            .format(len(episode_lists_new), mikan_id, len(anime_task_status_lists['suc'])))
                self.update_torrent_status(mikan_id, anime_task_status_lists['suc'])
            
            # 失败列表
            if len(anime_task_status_lists['failed']) > 0:
                self.logger.info("[do_anime_task][doAnimeTask][seed_schedule_task] Total {} new torrents of mikan_id {}, {} torrents fail to downloaded."\
                            .format(len(episode_lists_new), mikan_id, len(anime_task_status_lists['failed'])))

        totalTorrentInfos = self.getTotalTorrentInfos(self.anime_task)
        for mikan_id, torrentInfos in totalTorrentInfos.items():
            anime_name = self.mikan_id_to_name(mikan_id)
            for _, torrentInfo in torrentInfos.items():
                subgroup_name = self.subgroup_id_to_name(torrentInfo['subgroup_id'])
                torrentInfo['subgroupname'] = subgroup_name
            self.addTorrents(anime_name, torrentInfos)
            self.rename_torrent_file(anime_name, torrentInfos)

        end_time = time.time() - start_time
        self.logger.info("[do_anime_task][doAnimeTask][seed_schedule_task] seed_schedule_task cost time {}".format(end_time))

    def qb_status_schedule_task(self):
        torrents = self.qbt_client.torrents_info(filter='completed')
        for torrent in torrents:
            self.logger.info("[do_anime_task][doAnimeTask][qb_status_schedule_task] Task {} has been completed".\
                             format(torrent["name"]))
            self.update_qb_task_status(torrent["hash"])

class doTask(doAnimeTask, SpiderTask):
    def __init__(self, logger, mikan, anime_config, qb_cinfig, m_DBconnector, executor):
        doAnimeTask.__init__(self, logger, mikan, anime_config, qb_cinfig, m_DBconnector, executor)
        SpiderTask.__init__(self, mikan, m_DBconnector, logger)
    
    def createTask(self):
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info("[do_anime_task][doTask][createTask] Begin Task at {}".format(start_time))
        self.qb_status_schedule_task()
        self.update_anime_seed()
        self.seed_schedule_task()
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info("[do_anime_task][doTask][createTask] Finish Task at {}".format(end_time))

    def execAllTask(self, intervel):
        self.createTask()
        intervel = int(intervel)
        schedule.every(intervel).minutes.do(self.createTask)
        self.logger.info("[do_anime_task][doTask][execAllTask] scheduled task created successfully.")

        while True:
            self.logger.info("[do_anime_task][doTask][execAllTask] schedule task interval: {}".format(intervel))
            schedule.run_pending()
            time.sleep(2)