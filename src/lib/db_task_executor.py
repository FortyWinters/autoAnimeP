class DbTaskExecutor:
    def __init__(self, logger, m_db_connector):
        self.m_db_connector = m_db_connector
        self.logger = logger
        self.sub_mikan_id_lists = []
        self.mika_id_to_name_map = dict()

    def get_sub_mikan_id(self):
        sub_mikan_id_lists = []
        sql = 'select mikan_id from anime_list where subscribe_status=1'
        sub_mikan_id_lists.extend(item[0] for item in self.m_db_connector.execute(sql))  
        return sub_mikan_id_lists
    
    def get_mikan_id_by_anime_name(self, anime_name):
        sql = "select mikan_id from anime_list WHERE anime_name='{}'".format(anime_name)
        ret = self.m_db_connector.execute(sql)

        if len(ret) == 0 or ret[0][0] is None:
            return
        return ret[0][0]

    def create_mika_id_to_name_map(self, sub_mikan_id_lists):
        for mikan_id in sub_mikan_id_lists:
            sql = 'select anime_name from anime_list where mikan_id={}'.format(mikan_id)
            self.mika_id_to_name_map[mikan_id] = self.m_db_connector.execute(sql)[0][0]
        return self.mika_id_to_name_map
    
    def get_exist_anime_task_by_mikan_id(self, mikan_id):
        exist_anime_task = dict()
        sql = 'select episode,torrent_name,qb_task_status from anime_task where mikan_id={}'.\
            format(mikan_id)
        anime_tasks = self.m_db_connector.execute(sql)

        for anime_task in anime_tasks:
            episode = anime_task[0]
            torrent_name = anime_task[1]
            qb_task_status = anime_task[2]
            exist_anime_task[episode] = [torrent_name, qb_task_status]
        
        return exist_anime_task
    
    def get_total_anime_seed_by_mikan_id(self, mikan_id):
        total_anime_seed = []
        # TODO 添加 anime_seed 标记位，用来标识种子是否被消费过
        sql = 'select episode,seed_url,seed_status,subgroup_id from anime_seed where mikan_id={}'.format(mikan_id)
        anime_lists = self.m_db_connector.execute(sql)

        for anime_list in anime_lists:
            episode = anime_list[0]
            seed_url = anime_list[1]
            seed_status = anime_list[2]
            subgroup_id = anime_list[3]
            
            total_anime_seed.append([episode, seed_url, seed_status, subgroup_id])
        
        return total_anime_seed

    def delete_anime_task_by_mikan_id(self, mikan_id):
        sql = "DELETE FROM anime_task WHERE mikan_id={}".format(mikan_id)
        self.m_db_connector.execute(sql)

    def update_torrent_status(self,
                              mikan_id,
                              anime_task_status_lists):
        
        for anime_seed_task_attr in anime_task_status_lists:
            # torrent_name = torrent_name.split('/')[3]
            episode = anime_seed_task_attr[0]
            torrent_name = anime_seed_task_attr[1]

            sql = "INSERT INTO anime_task (mikan_id, qb_task_status, episode, torrent_name) VALUES ({}, {}, {}, '{}')".\
                format(mikan_id, 0, episode, torrent_name)
            self.m_db_connector.execute(sql)

    def check_torrent_status(self,
                              mikan_id,
                              anime_task_status_lists):
        
        for anime_seed_task_attr in anime_task_status_lists:
            # torrent_name = torrent_name.split('/')[3]
            episode = anime_seed_task_attr[0]
            torrent_name = anime_seed_task_attr[1]

            sql = sql = "select * from anime_task WHERE mikan_id={} and episode={}".format(mikan_id, episode)
            
            try:
                ret = self.m_db_connector.execute(sql)
            except Exception as e:
                self.logger.warning("[DbTaskExecutor][check_torrent_status] fail to find any item by mikan_id={} and episode={}".\
                                  format(mikan_id, episode))
                continue

            if len(ret) != 0:
                continue

            sql = "INSERT INTO anime_task (mikan_id, qb_task_status, episode, torrent_name) VALUES ({}, {}, {}, '{}')".\
                format(mikan_id, 1, episode, torrent_name)
            self.m_db_connector.execute(sql)

    def update_seed_status(self, seed_url):
        sql = "UPDATE anime_seed SET seed_status=1 WHERE seed_url='{}'".format(seed_url)
        self.m_db_connector.execute(sql)
    
    def update_qb_task_status(self, torrent_hash):
        sql = "UPDATE anime_task SET qb_task_status=1 WHERE torrent_name LIKE '%{}%'".format(torrent_hash)
        self.m_db_connector.execute(sql)

    def subgroup_id_to_name(self, subgroup_id):
        sql = "select subgroup_name from anime_subgroup WHERE subgroup_id={}".format(subgroup_id)
        subgroup_name = self.m_db_connector.execute(sql)[0][0]
        return subgroup_name
    
    # 局部filter
    def add_episode_offset_filter_by_mikan_id(self, mikan_id, episode_offset):
        sql = "select * from anime_filter WHERE mikan_id={} and filter_type='episode_offset'".format(mikan_id)
        ret = self.m_db_connector.execute(sql)

        if len(ret) == 0:
            sql = "INSERT INTO anime_filter (mikan_id, filter_val, filter_type) VALUES ({}, {}, 'episode_offset')".format(mikan_id, episode_offset)
        else:
            sql = "UPDATE anime_filter SET filter_val={} WHERE mikan_id={} and filter_type='episode_offset'".format(episode_offset, mikan_id)
        self.m_db_connector.execute(sql)
    
    def add_skip_subgroup_filter_by_mikan_id(self, mikan_id, skip_subgroup):
        sql = "select * from anime_filter WHERE mikan_id={} and filter_val={}".format(mikan_id, skip_subgroup)
        ret = self.m_db_connector.execute(sql)
        
        if len(ret) > 0:
            return
        sql = "INSERT INTO anime_filter (mikan_id, filter_val, filter_type) VALUES ({}, {}, 'skip_subgroup')".format(mikan_id, skip_subgroup)
        self.m_db_connector.execute(sql)

    def del_episode_offset_filter_by_mikan_id(self, mikan_id):
        sql = "DELETE FROM anime_filter WHERE mikan_id={} and filter_type='episode_offset'".format(mikan_id)
        self.m_db_connector.execute(sql)
    
    def del_skip_subgroup_filter_by_mikan_id(self, mikan_id):
        sql = "DELETE FROM anime_filter WHERE mikan_id={} and filter_type='skip_subgroup'".format(mikan_id)
        self.m_db_connector.execute(sql)

    def del_skip_subgroup_filter_by_mikan_id_and_skip_subgroup(self, mikan_id, skip_subgroup):
        sql = "DELETE FROM anime_filter WHERE mikan_id={} and filter_type='skip_subgroup' and filter_val={}".format(mikan_id, skip_subgroup)
        self.m_db_connector.execute(sql)

    def get_episode_offset_filter_by_mikan_id(self, mikan_id):
        sql = "select filter_val from anime_filter WHERE mikan_id={} and filter_type='episode_offset'".format(mikan_id)
        ret = self.m_db_connector.execute(sql)
        return ret[0][0]
    
    def get_skip_subgroup_filter_by_mikan_id(self, mikan_id):
        sql = "select filter_val from anime_filter WHERE mikan_id={} and filter_type='skip_subgroup'".format(mikan_id)
        ret = self.m_db_connector.execute(sql)
        return ret
    
    # 全局filter
    def add_global_episode_offset_filter(self, episode_offset):
        sql = "select * from anime_filter WHERE object=1 and filter_type='episode_offset'"
        ret = self.m_db_connector.execute(sql)

        if len(ret) == 0:
            sql = "INSERT INTO anime_filter (mikan_id, filter_val, filter_type, object) VALUES (0, {}, 'episode_offset', 1)".format(episode_offset)
        else:
            sql = "UPDATE anime_filter SET filter_val={} WHERE object=1 and filter_type='episode_offset'".format(episode_offset)
        self.m_db_connector.execute(sql)
    
    def add_global_skip_subgroup_filter_filter(self, skip_subgroup):
        sql = "select * from anime_filter WHERE object=1 and filter_val={}".format(skip_subgroup)
        ret = self.m_db_connector.execute(sql)
        
        if len(ret) > 0:
            return
        sql = "INSERT INTO anime_filter (mikan_id, filter_val, filter_type, object) VALUES (0, {}, 'skip_subgroup', 1)".format(skip_subgroup)
        self.m_db_connector.execute(sql)
    
    def del_global_episode_offset_filter(self):
        sql = "DELETE FROM anime_filter WHERE object=1 and filter_type='episode_offset'"
        self.m_db_connector.execute(sql)
    
    def del_global_skip_subgroup_filter(self):
        sql = "DELETE FROM anime_filter WHERE object=1 and filter_type='skip_subgroup'"
        self.m_db_connector.execute(sql)
    
    def del_global_skip_subgroup_filter_by_skip_subgroup(self, skip_subgroup):
        sql = "DELETE FROM anime_filter WHERE object=1 and filter_type='skip_subgroup' and filter_val={}".format(skip_subgroup)
        self.m_db_connector.execute(sql)
    
    def get_global_episode_offset_filter(self):
        sql = "select filter_val from anime_filter WHERE object=1 and filter_type='episode_offset'"
        ret = self.m_db_connector.execute(sql)
        return ret[0][0]

    def get_global_skip_subgroup_filter(self):
        sql = "select filter_val from anime_filter WHERE object=1 and filter_type='skip_subgroup'"
        ret = self.m_db_connector.execute(sql)
        return ret