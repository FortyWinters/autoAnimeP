import os
import sys
from concurrent.futures import wait, ALL_COMPLETED

class AddAnimeTask:
    def __init__(self, logger, executor, m_mikan, anime_task_config):
        self.logger = logger
        self.executor = executor
        self.m_mikan = m_mikan
        self.config = anime_task_config
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

    # exist_anime_task_cur_mikan_id : {episode, [torrent_name, qb_task_status]}
    # total_anime_seed_cur_mikan_id : {episode, torrent_name}
    def update_anime_tasks_by_mikan_id(self, mikan_id, 
                                       exist_anime_task_cur_mikan_id, 
                                       total_anime_seed_cur_mikan_id):

        anime_task_cur_mikan_id = dict()

        for anime_list in total_anime_seed_cur_mikan_id:
            episode = anime_list[0]
            seed_status = anime_list[2]
            # 跳过：
            # 1. 已经添加过的种子
            # 2. 下载成功的种子
            if (episode in anime_task_cur_mikan_id) or \
                (episode in exist_anime_task_cur_mikan_id) or \
                (seed_status == 1) :
                continue
            torrent_name = anime_list[1]
            anime_task_cur_mikan_id[episode] = torrent_name
        
        self.anime_task[mikan_id] = anime_task_cur_mikan_id

    def download_anime_seed_by_mikan_id_task(self, mikan_id, episode_lists_new):
        dir = self.config['SEED'] + str(mikan_id) + "/"
        anime_task_status = dict()
        anime_seed_task_list_suc = []
        anime_seed_task_list_failed = []
        all_tasks = []

        if not os.path.exists(dir):
            os.makedirs(dir)
        
        for episode, torrent_name in episode_lists_new.items():
            task = self.executor.submit(self.download_anime_seed_thread,
                                        (dir, 
                                         episode,
                                         torrent_name, 
                                         anime_seed_task_list_suc,  
                                         anime_seed_task_list_failed ))
            all_tasks.append(task)

        wait(all_tasks, return_when=ALL_COMPLETED)

        anime_task_status['suc'] = anime_seed_task_list_suc
        anime_task_status['failed'] = anime_seed_task_list_failed
        
        return anime_task_status
    
    def download_anime_seed_thread(self, args):
        dir, episode, torrent_name, anime_seed_task_list_suc, anime_seed_task_list_failed = args
        
        anime_seed_task_attr = []
        anime_seed_task_attr.append(episode)
        anime_seed_task_attr.append(torrent_name)

        if self.m_mikan.download_seed(torrent_name, dir):
            anime_seed_task_list_suc.append(anime_seed_task_attr)
        else:
            anime_seed_task_list_failed.append(anime_seed_task_attr)
            self.logger.warning("[addAnimeTask] download seed {} failed.".format(torrent_name))