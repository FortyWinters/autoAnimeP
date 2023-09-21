import os
import sys
from lib.connect import m_DBconnector
from lib.spider import m_mikan
from lib.logManager import m_LogManager
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED


class AddAnimeTask:
    def __init__(self, logger, executor):
        self.logger = logger
        self.executor = executor
        self.mikan_id_lists = []
        self.mika_id_to_name_map = dict()

        # animeTask : {mikan_id, {episode, torrent_name}}
        self.anime_task = dict()
    
    def mikan_id_to_name(self, mikan_id):
        if mikan_id in self.mika_id_to_name_map:
            return self.mika_id_to_name_map[mikan_id]
        else:
            self.logger.error("[addAnimeTask] failed to get anime name by mikan_id {} .".format(mikan_id))
            sys.exit(0)

    def print_all_sub_anime_name(self):
        for mikan_id in self.mikan_id_lists:
            print(mikan_id, self.mikan_id_to_name(mikan_id))

    # exist_anime_task_cur_mikan_id : {episode, torrent_name}
    # total_anime_seed_cur_mikan_id : {episode, torrent_name}
    def update_anime_tasks_by_mikan_id(self, mikan_id, 
                                       exist_anime_task_cur_mikan_id, 
                                       total_anime_seed_cur_mikan_id):

        anime_task_cur_mikan_id = dict()

        for anime_list in total_anime_seed_cur_mikan_id:
            episode = anime_list[0]
            if episode in anime_task_cur_mikan_id or episode in exist_anime_task_cur_mikan_id:
                continue
            torrent_name = anime_list[1]
            anime_task_cur_mikan_id[episode] = torrent_name
        
        self.anime_task[mikan_id] = anime_task_cur_mikan_id

    def download_anime_seed_by_mikan_id_task(self, mikan_id, episode_lists_new):
        dir = "seed/" + str(mikan_id) + "/"
        anime_task_status = dict()
        anime_seed_task_list_suc = []
        anime_seed_task_list_failed = []
        all_tasks = []

        if not os.path.exists(dir):
            os.makedirs(dir)
        
        for episode, torrent_name in episode_lists_new.items():
            task = self.executor.submit(self.download_anime_seed_thread, 
                                        (dir, torrent_name, 
                                         anime_seed_task_list_suc,  
                                         anime_seed_task_list_failed ))
            all_tasks.append(task)

        wait(all_tasks, return_when=ALL_COMPLETED)

        anime_task_status['suc'] = anime_seed_task_list_suc
        anime_task_status['failed'] = anime_seed_task_list_failed
        
        return anime_task_status
    
    def download_anime_seed_thread(self, args):
        dir, torrent_name, anime_seed_task_list_suc,  anime_seed_task_list_failed = args
        
        if m_mikan.download_seed(torrent_name, dir):
            anime_seed_task_list_suc.append(torrent_name)
        else:
            anime_seed_task_list_failed.append(torrent_name)
            self.logger.warning("[addAnimeTask] download seed {} failed.".format(torrent_name))
    
    # def re_download__anime_seed_task

# logger = m_LogManager.getLogObj(sys.argv[0])
# m_addAnimeTask= AddAnimeTask(logger)

# m_addAnimeTask.printAllSubscribeAnimeName()
# m_addAnimeTask.getAnimeTaskByMikanId(3060)

# m_addAnimeTask.run()
# m_addAnimeTask.printAnimeTask()
# m_addAnimeTask.deletAllTask()