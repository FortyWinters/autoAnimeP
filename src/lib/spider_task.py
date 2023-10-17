import sys
from concurrent.futures import wait, ALL_COMPLETED
from .common import Seed

QUERY_ANIME_BY_SUBSCRIBE_STATUS = "SELECT mikan_id, anime_type FROM anime_list WHERE subscribe_status=1"
QUERY_SEED_BY_MIKAN_ID = "SELECT mikan_id, episode, seed_url, subgroup_id, seed_name, seed_status, seed_size FROM anime_seed WHERE mikan_id={}"
QUERY_SUBGROUP = "SELECT subgroup_id FROM anime_subgroup"
INSERT_SEED_INFO = "INSERT INTO anime_seed (mikan_id, episode, seed_url, subgroup_id, seed_name, seed_status, seed_size) VALUES {}"
INSERT_SUBGROUP_INFO = "INSERT INTO anime_subgroup (subgroup_id, subgroup_name) VALUES {}"

class SpiderTask:
    def __init__(self, mikan, db, logger, executor):
        self.mikan = mikan
        self.db = db
        self.logger = logger
        self.executor = executor
        self.subgroup_id_set = set()
        self.init_subgroup_id_set()
    
    def query_subscribe_anime_list(self):
        try:
            query_res = self.db.execute(QUERY_ANIME_BY_SUBSCRIBE_STATUS)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] query_subscribe_anime_list failed, error: {}".format(e))
        else:
            subscribe_anime_list = []
            for a in query_res:
                subscribe_anime_list.append({"mikan_id": a[0], "anime_type": a[1]})
            return subscribe_anime_list
    
    def query_seed_list_by_mikan_id(self, mikan_id):
        sql = QUERY_SEED_BY_MIKAN_ID.format(mikan_id)
        try:
            query_res = self.db.execute(sql)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] query_seed_list_by_mikan_id, error: {}".format(e))
            return False
        else:
            return query_res
    
    def query_anime_subgroup(self):
        try:
            query_res = self.db.execute(QUERY_SUBGROUP)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] query_anime_subgroup failed, error: {}".format(e))
        else:
            subgroup_list = []
            for a in query_res:
                subgroup_list.append(a[0])
            return subgroup_list
        
    def insert_seed_info(self, seed_info_str):
        if seed_info_str == '':
            return True
        sql = INSERT_SEED_INFO.format(seed_info_str)
        try:
            self.db.execute(sql)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] insert_seed_info failed, error: {}".format(e))
            return False
        else:
            return True

    def insert_subgroup_info(self, subgroup_info_str):
        if subgroup_info_str == '':
            return True
        sql = INSERT_SUBGROUP_INFO.format(subgroup_info_str)
        try:
            self.db.execute(sql)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] insert_subgroup_info failed, error: {}".format(e))
            return False
        else:
            return True
        
    def seed_list_to_seed_info_str(self, seed_list):
        seed_info_str = ''
        for s in seed_list:
            seed_info_str += "{},".format(s.to_string())
        return seed_info_str[:-1]

    def subgroup_list_to_subgroup_info_str(self, subgroup_list):
        subgroup_info_str = ''
        for s in subgroup_list:
            subgroup_info_str += "{},".format(s.to_string())
        return subgroup_info_str[:-1]
    
    def init_subgroup_id_set(self):
        try:
            subgroup_list = self.query_anime_subgroup()
            for s in subgroup_list:
                if s not in self.subgroup_id_set:
                    self.subgroup_id_set.add(s)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] init_subgroup_id_set failed, error: {}".format(e))
            sys.exit(0)

    def get_seed_list_old(self, mikan_id):
        seed_list_old = []
        try:
            query_res = self.query_seed_list_by_mikan_id(mikan_id)
            for s in query_res:
                seed = Seed(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
                seed_list_old.append(seed)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] get_seed_list_old failed, mikan_id: {}, error: {}".format(mikan_id, e))
        return seed_list_old

    def get_seed_list_new(self, mikan_id, anime_type):
        seed_list_new = []
        try:
            subgroup_list = self.mikan.get_subgroup_list(mikan_id)
            subgroup_list_update = []
            for s in subgroup_list:
                if s.subgroup_id not in self.subgroup_id_set:
                    self.subgroup_id_set.add(s.subgroup_id)
                    subgroup_list_update.append(s)

            subgroup_info_str = self.subgroup_list_to_subgroup_info_str(subgroup_list_update)
            self.insert_subgroup_info(subgroup_info_str)

            seed_list_new = self.mikan.get_seed_list_task(mikan_id, subgroup_list, anime_type)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] get_seed_list_new failed, mikan_id: {}, error: {}".format(mikan_id, e))
        else:
            return seed_list_new

    def get_seed_list_update(self, mikan_id, anime_type):
        seed_set_update = []
        try:
            seed_list_old = self.get_seed_list_old(mikan_id)
            seed_list_new = self.get_seed_list_new(mikan_id, anime_type)
            seed_set_update = set(seed_list_new) - set(seed_list_old)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] get_seed_list_update failed, mikan_id: {}, error: {}".format(mikan_id, e))
        else:
            return list(seed_set_update)
    
    # 遍历番剧列表无法跑满线程池，使用的线程数取决于番剧的字幕组数
    def update_anime_seed(self):
        try:
            anime_list = self.query_subscribe_anime_list()
            for a in anime_list:
                mikan_id = a["mikan_id"]
                anime_type = a["anime_type"]
                seed_list_update = self.get_seed_list_update(mikan_id, anime_type)
                seed_info_str = self.seed_list_to_seed_info_str(seed_list_update)
                if not self.insert_seed_info(seed_info_str):
                    continue
        except Exception as e:
            self.logger.warning("[SPIDERTASK] update_anime_seed failed, error: {}".format(e))
            return False
        return True
    
    def get_anime_subgroup_list_thread(self, args):
        try:
            mikan_id, anime_type, anime_subgroup_list = args
            self.logger.info("[SPIDERTASK] get_anime_subgroup_list_thread, mikan_id: {}, anime_type: {}".format(mikan_id, anime_type))

            subgroup_list = self.mikan.get_subgroup_list(mikan_id)
            for s in subgroup_list:  
                anime_subgroup_list.append({"mikan_id": mikan_id, "anime_type": anime_type, "subgroup": s})
        except Exception as e:
            self.logger.warning("[SPIDERTASK] get_anime_subgroup_list_thread failed, mikan_id: {}, anime_type: {}, error: {}".format(mikan_id, anime_type, e))

    def get_anime_subgroup_list_task(self, anime_list):
        try:
            self.logger.info("[SPIDERTASK] get_anime_subgroup_list_task start, anime number: {}".format(len(anime_list)))
            anime_subgroup_list = []
            task_list = []
            for a in anime_list:
                task = self.executor.submit(self.get_anime_subgroup_list_thread, (a["mikan_id"], a["anime_type"], anime_subgroup_list))
                task_list.append(task)
            wait(task_list, return_when=ALL_COMPLETED)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] get_anime_subgroup_list_task, error: {}".format(e))        
        else:
            self.logger.info("[SPIDERTASK] get_anime_subgroup_list_task finished, anime number: {}".format(len(anime_list)))
            return anime_subgroup_list

    def get_seed_list_new_thread(self, args):
        try:
            mikan_id, subgroup_id, anime_type, anime_seed_dict_list = args
            self.logger.info("[SPIDERTASK] get_seed_list_new_thread, mikan_id: {}, subgroup_id: {}, anime_type: {}".format(mikan_id, subgroup_id, anime_type))

            seed_list_new = self.mikan.get_seed_list(mikan_id, subgroup_id, anime_type)
            anime_seed_dict_list.append({"mikan_id": mikan_id, "seed_list_new": seed_list_new})
        except Exception as e:
            self.logger.warning("[SPIDERTASK] get_seed_list_new_thread failed, mikan_id: {}, subgroup_id: {}, anime_type: {}, error: {}".format(mikan_id, subgroup_id, anime_type, e))
        
    def get_seed_list_new_task(self, anime_subgroup_list):
        self.logger.info("[SPIDERTASK] get_seed_list_new_task start")
        try:
            anime_seed_dict_list = []
            task_list = []
            for a in anime_subgroup_list:
                task = self.executor.submit(self.get_seed_list_new_thread, (a["mikan_id"], a["subgroup"].subgroup_id, a["anime_type"], anime_seed_dict_list))
                task_list.append(task)
            wait(task_list, return_when=ALL_COMPLETED)
        except Exception as e:
            self.logger.warning("[SPIDERTASK] get_seed_list_new_task failed, error: {}".format(e))
        else:
            self.logger.info("[SPIDERTASK] get_seed_list_new_task finished")
            return anime_seed_dict_list

    # 跑满线程池
    def update_anime_seed_full_speed(self):
        try:
            # 爬取番剧字幕组信息
            anime_list = self.query_subscribe_anime_list()
            anime_subgroup_list = self.get_anime_subgroup_list_task(anime_list)
            subgroup_list = [a["subgroup"] for a in anime_subgroup_list]
            unique_subgroup_list = list(set(subgroup_list))
            subgroup_list_update = []
            for s in unique_subgroup_list:
                if s.subgroup_id not in self.subgroup_id_set:
                    self.subgroup_id_set.add(s.subgroup_id)
                    subgroup_list_update.append(s)

            subgroup_info_str = self.subgroup_list_to_subgroup_info_str(subgroup_list_update)
            self.insert_subgroup_info(subgroup_info_str)

            # 爬取番剧种子
            seed_dict_list = self.get_seed_list_new_task(anime_subgroup_list)

            for a in seed_dict_list:
                seed_list_old = self.get_seed_list_old(a["mikan_id"])
                a["seed_list_old"] = seed_list_old

            for a in seed_dict_list:
                seed_set_update = []
                seed_list_old = a["seed_list_old"]
                seed_list_new = a["seed_list_new"]
                seed_set_update = set(seed_list_new) - set(seed_list_old)
                seed_list_update = list(seed_set_update)
                seed_info_str = self.seed_list_to_seed_info_str(seed_list_update)
                if not self.insert_seed_info(seed_info_str):
                    continue
        except Exception as e:
            self.logger.warning("[SPIDERTASK] update_anime_seed_full_speed failed, error: {}".format(e))
            return False
        return True