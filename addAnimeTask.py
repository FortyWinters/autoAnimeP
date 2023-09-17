import os
from lib.connect import m_DBconnector
from lib.spider import m_mikan


class AddAnimeTask:
    def __init__(self):
        self.mikan_id_lists = []
        self.isUpdate = False

        # animeTask : {mikan_id, {episode, seed_url}}
        self.animeTask = dict()
        
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
        self.animeTask.clear()

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

        # 下载种子, 并回写 anime_list
        dir = "seed/" + str(mikan_id) + "/"
        for episode, seed_url in anime_task_episode_lists_new.items():
            if not os.path.exists(dir):
                os.makedirs(dir)
            m_mikan.download_seed(seed_url, dir)
            self.animeTask[mikan_id] = anime_task_episode_lists_new

            torrent_name = seed_url.split('/')[3]
            sql = "INSERT INTO anime_task (mikan_id, status, episode, torrent_name) VALUES ({}, {}, {}, '{}')".format(mikan_id, 0, episode, torrent_name)
            m_DBconnector.execute(sql)

        return anime_task_episode_lists_new

    def printAnimeTask(self):
        if not self.isUpdate:
            print("[INFO] Please exec self.run() to update anime tasks before printAnimeTask.")
            return False
        
        if len(self.animeTask) == 0:
            print("[INFO] No new tasks.")
            return True
        
        for mikan_id, episode_map in self.animeTask.items():
            print(mikan_id)
            for episode, seed_url in episode_map.items():
                print(episode, seed_url)
        self.isUpdate = False
        return True

    def run(self):
        for mikan_id in self.mikan_id_lists:
            self.getAnimeTaskByMikanId(mikan_id)
        self.isUpdate = True

m_AddAnimeTask= AddAnimeTask()

m_AddAnimeTask.printAllSubscribeAnimeName()
m_AddAnimeTask.run()
m_AddAnimeTask.printAnimeTask()
# AddAnimeTask().getAnimeTaskByMikanId(3060)
# AddAnimeTask().run()