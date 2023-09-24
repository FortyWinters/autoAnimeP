from .connect import DBconnect

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
    
    def create_mika_id_to_name_map(self, sub_mikan_id_lists):
        for mikan_id in sub_mikan_id_lists:
            sql = 'select anime_name from anime_list where mikan_id={}'.format(mikan_id)
            self.mika_id_to_name_map[mikan_id] = self.m_db_connector.execute(sql)[0][0]
        return self.mika_id_to_name_map
    
    def get_exist_anime_task_by_mikan_id(self, mikan_id):
        exist_anime_task = dict()
        sql = 'select episode,torrent_name,torrent_status,qb_task_status from anime_task where mikan_id={}'.\
            format(mikan_id)
        anime_tasks = self.m_db_connector.execute(sql)

        for anime_task in anime_tasks:
            episode = anime_task[0]
            torrent_name = anime_task[1]
            torrent_status = anime_task[2]
            qb_task_status = anime_task[3]
            exist_anime_task[episode] = [torrent_name, torrent_status, qb_task_status]
        
        return exist_anime_task
    
    def get_total_anime_seed_by_mikan_id(self, mikan_id):
        total_anime_seed = dict()
        # TODO 添加 anime_seed 标记位，用来标识种子是否被消费过
        sql = 'select episode,seed_url from anime_seed where mikan_id={}'.format(mikan_id)
        anime_lists = self.m_db_connector.execute(sql)

        for anime_list in anime_lists:
            episode = anime_list[0]
            seed_url = anime_list[1]
            total_anime_seed[episode] = seed_url
        
        return anime_lists

    def delete_anime_task_by_mikan_id(self, mikan_id):
        sql = "DELETE FROM anime_task WHERE mikan_id={}".format(mikan_id)
        self.m_db_connector.execute(sql)

    def update_torrent_status(self,
                              mikan_id,
                              anime_task_status_lists, 
                              is_successed):
        
        torrent_status = 0
        for anime_seed_task_attr in anime_task_status_lists:
            # torrent_name = torrent_name.split('/')[3]
            episode = anime_seed_task_attr[0]
            torrent_name = anime_seed_task_attr[1]

            if is_successed:
                torrent_status = 1
            sql = "INSERT INTO anime_task (mikan_id, torrent_status, qb_task_status, episode, torrent_name) VALUES ({}, {}, {}, {}, '{}')".\
                format(mikan_id, torrent_status, 0, episode, torrent_name)
            self.m_db_connector.execute(sql)

    