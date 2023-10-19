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

        # animeTask : {mikan_id, {episode, [torrent_name, subgroupname]]}}
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
    # total_anime_seed_cur_mikan_id : [episode, seed_url, seed_status, subgroup_id]
    def update_anime_tasks_by_mikan_id(self, 
                                       mikan_id, 
                                       exist_anime_task_cur_mikan_id, 
                                       total_anime_seed_cur_mikan_id):

        anime_task_cur_mikan_id = dict()

        for seed_info in total_anime_seed_cur_mikan_id:
            episode = seed_info[0]
            torrent_name = seed_info[1]
            seed_status = seed_info[2]
            subgroup_id = seed_info[3]

            # 跳过：
            # 1. 已经添加过的种子
            # 2. 下载成功的种子
            if (episode in anime_task_cur_mikan_id) or (episode in exist_anime_task_cur_mikan_id) or \
                (seed_status == 1) :
                self.logger.debug("[addAnimeTask] skip used torrent: {}.".format(torrent_name))
                continue
            seed_info_cur_mikanId_and_episode = [torrent_name, subgroup_id]
            anime_task_cur_mikan_id[episode] = seed_info_cur_mikanId_and_episode
        
        self.anime_task[mikan_id] = anime_task_cur_mikan_id
    
    def update_anime_tasks_by_mikan_id_with_filter(self, 
                                                   mikan_id, 
                                                   exist_anime_task_cur_mikan_id, 
                                                   total_anime_seed_cur_mikan_id,
                                                   global_filter,
                                                   local_filter):

        anime_task_cur_mikan_id = dict()

        episode_offset = global_filter['episode_offset']
        skip_subgroup = global_filter['skip_subgroup']

        if local_filter['episode_offset'] is not None:
            episode_offset = local_filter['episode_offset']
        if local_filter['skip_subgroup'] is not None:
            skip_subgroup = local_filter['skip_subgroup']

        print(episode_offset, skip_subgroup)

        for seed_info in total_anime_seed_cur_mikan_id:
            episode = seed_info[0]
            torrent_name = seed_info[1]
            seed_status = seed_info[2]
            subgroup_id = seed_info[3]

            # 跳过：
            # 1. 已经添加过的种子
            # 2. 下载成功的种子
            # 3. 需要跳过的字幕组的种子
            # 4. 预设起始集数前的种子
            if (episode in anime_task_cur_mikan_id) or (episode in exist_anime_task_cur_mikan_id) or \
                (seed_status == 1) or \
                (subgroup_id in skip_subgroup) or \
                (episode < episode_offset):
                self.logger.debug("[addAnimeTask] skip used torrent: {}.".format(torrent_name))
                continue
            seed_info_cur_mikanId_and_episode = [torrent_name, subgroup_id]
            anime_task_cur_mikan_id[episode] = seed_info_cur_mikanId_and_episode
        
        self.anime_task[mikan_id] = anime_task_cur_mikan_id

    def download_anime_seed_by_mikan_id_task(self, mikan_id, episode_lists_new):
        dir = self.config['SEED'] + str(mikan_id) + "/"
        anime_task_status = dict()
        anime_seed_task_list_suc = []
        anime_seed_task_list_failed = []
        all_tasks = []

        if not os.path.exists(dir):
            os.makedirs(dir)
        
        for episode, torrent_info in episode_lists_new.items():
            task = self.executor.submit(self.download_anime_seed_thread,
                                        (dir, 
                                         episode,
                                         torrent_info[0], 
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