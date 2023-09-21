import sys
from lib.spider_task import SpiderTask
from lib.spider import Mikan
from lib.config import m_config
from lib.logManager import m_LogManager
from lib.connect import m_DBconnector
import time

spider_config = m_config.get('SPIDER')
logger = m_LogManager.getLogObj(sys.argv[0])
db = m_DBconnector

mikan = Mikan(logger, spider_config)
spider_task = SpiderTask(mikan, db, logger)

def test():
    # anime_list = spider_task.query_subscribe_anime_list()
    # print(anime_list)

    # seed_list_old = spider_task.get_seed_list_old(3060)
    # print(seed_list_old)

    # seed_list_new = spider_task.get_seed_list_new(3060)
    # print(seed_list_new)

    # seed_list_update = spider_task.get_seed_list_update(3060)
    # print(len(seed_list_update))

    # seed_info_str = spider_task.seed_list_to_seed_info_str(seed_list_update)
    # print(seed_info_str)

    # spider_task.insert_seed_info(seed_info_str)
    # print("ok")
    
    start_time = time.time()
    spider_task.update_anime_seed()
    print("ok")
    print(time.time()-start_time)

if __name__ == '__main__':
    test()