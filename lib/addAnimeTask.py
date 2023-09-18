import os
import sys
from lib.connect import m_DBconnector
from lib.spider import m_mikan
from lib.logManager import m_LogManager

class AddAnimeTask:
    def __init__(self, logger):
        self.logger = logger
        self.mikan_id_lists = []
        
        # TODO 定时老化
        self.isUpdate = False

        # animeTask : {mikan_id, {episode, seed_url}}
        self.anime_task = dict()
        
        self.updateSubscribeAnime()

    def updateSubscribeAnime(self):
        sql = 'select mikan_id from anime_list where subscribe_status=1'
        self.mikan_id_lists.extend(item[0] for item in m_DBconnector.execute(sql))  
    
    def mikanIdToName(self, mikan_id):
        sql = 'select anime_name from anime_list where mikan_id={}'.format(mikan_id)
        anime_name = m_DBconnector.execute(sql)[0][0]
        # print(anime_name)
        return anime_name

    def printAllSubscribeAnimeName(self):
        for mikan_id in  self.mikan_id_lists:
            self.mikanIdToName(mikan_id)
            print(mikan_id, self.mikanIdToName(mikan_id))
    
    def getAnimeTaskByMikanId(self, mikan_id):
        # 获取已经添加的任务
        # anime_task_episode_lists_old : {episode, status}
        anime_task_episode_lists_old = dict()
        sql = 'select episode,status from anime_task where mikan_id={}'.format(mikan_id)
        anime_tasks = m_DBconnector.execute(sql)
        
        for anime_task in anime_tasks:
            episode = anime_task[0]
            status = anime_task[1]
            anime_task_episode_lists_old[episode] = status
        
        # print(anime_task_episode_lists_old)
        
        # 获取所有可以下载的剧集并去重
        # anime_task_episode_lists_new : {episode, seed_url}
        anime_task_episode_lists_new = dict()
        sql = 'select episode,seed_url from anime_seed where mikan_id={}'.format(mikan_id)
        anime_lists = m_DBconnector.execute(sql)

        for anime_list in anime_lists:
            episode = anime_list[0]
            if episode in anime_task_episode_lists_new or episode in anime_task_episode_lists_old:
                continue
            seed_url = anime_list[1]
            anime_task_episode_lists_new[episode] = seed_url
        
        # print(anime_task_episode_lists_new)

        # 下载种子, 并回写 anime_task
        anime_task_cache = self.downloadAnimeSeed(mikan_id, anime_task_episode_lists_new)

        re_download_times =  2
        while len(anime_task_cache) > 0 and re_download_times > 0:
            anime_task_cache = self.downloadAnimeSeed(mikan_id, anime_task_episode_lists_new)
            re_download_times = re_download_times - 1

        if not self.isUpdate:
            self.isUpdate = True
    
    def downloadAnimeSeed(self, mikan_id, anime_task_episode_lists_new):
        dir = "seed/" + str(mikan_id) + "/"
        anime_task_cache = dict()
        for episode, seed_url in anime_task_episode_lists_new.items():
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            if m_mikan.download_seed(seed_url, dir):
                torrent_name = seed_url.split('/')[3]
                sql = "INSERT INTO anime_task (mikan_id, status, episode, torrent_name) VALUES ({}, {}, {}, '{}')".format(mikan_id, 0, episode, torrent_name)
                m_DBconnector.execute(sql)
        
                self.anime_task[mikan_id] = anime_task_episode_lists_new
            else:
                anime_task_cache[episode] = seed_url
                logger.warning("[addAnimeTask] download seed {} failed.".format(seed_url))
        
        return anime_task_cache

    def deleteTaskByMikanId(self, mikan_id):
        sql = "DELETE FROM anime_task WHERE mikan_id={}".format(mikan_id)
        m_DBconnector.execute(sql)
        return True

    def printAnimeTask(self):
        if not self.isUpdate:
            logger.warning("Please exec self.getAnimeTaskByMikanId() to update anime tasks before printAnimeTask.")
            return False
        
        if len(self.anime_task) == 0:
            logger.info("[INFO] No new tasks.")
            return True

        for mikan_id, episode_map in self.anime_task.items():
            if len(episode_map) == 0:
                continue
            print(mikan_id, self.mikanIdToName(mikan_id))
            for episode, seed_url in episode_map.items():
                print(episode, seed_url)
        
        return True

    def getAllAnimeTask(self):
        for mikan_id in self.mikan_id_lists:
            self.getAnimeTaskByMikanId(mikan_id)

    def deletAllTask(self):
        for mikan_id in self.mikan_id_lists:
            self.deleteTaskByMikanId(mikan_id)

logger = m_LogManager.getLogObj(sys.argv[0])
m_addAnimeTask= AddAnimeTask(logger)

# m_addAnimeTask.printAllSubscribeAnimeName()
# m_addAnimeTask.getAnimeTaskByMikanId(3060)

# m_addAnimeTask.run()
# m_addAnimeTask.printAnimeTask()
# m_addAnimeTask.deletAllTask()