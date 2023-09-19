import threading
from lib.spider import Mikan
from lib.logManager import m_LogManager
import time

time_list = []

def spiderTask(mikan_id, subgroup_id):
    seed_list = mikan.get_seed_list(mikan_id, subgroup_id)
    time_list.append(time.time())
    print("[T]subgroup_id: {}, seed_list length: {}".format(subgroup_id, len(seed_list)))
    

def runSpiderTask(mikan_id, subgroup_list):
    for sub in subgroup_list:
        t = threading.Thread(target=spiderTask, args=(mikan_id, sub.subgroup_id,))
        t.start()

def compare():
    mikan = Mikan(m_LogManager)
    subgroup_list = mikan.get_subgroup_list(3060)

    start_time_t = time.time()
    runSpiderTask(3060, subgroup_list)

    time.sleep(20)

    start_time = time.time()
    for sub in subgroup_list:
        seed_list = mikan.get_seed_list(3060, sub.subgroup_id)
        print("[S]subgroup_id: {}, seed_list length: {}".format(sub.subgroup_id, len(seed_list)))
    print("[S]spider: {}".format(time.time() - start_time))
    print("[T]spider_t: {}".format(max(time_list) - start_time_t))

def spider_thread():
    mikan = Mikan(m_LogManager)
    mikan_id=3071
    subgroup_list = mikan.get_subgroup_list(mikan_id)
    start_time = time.time()
    seed_list = mikan.get_seed_list_thread_task(mikan_id, subgroup_list)
    print(len(seed_list))
    print("time: {}".format(time.time() - start_time))

if __name__ == '__main__':
    spider_thread()