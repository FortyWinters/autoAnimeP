import sys
import timeit
from lib.common import Seed

mikan_id = 3080
episode = 12
seed_url = '/Download/20230918/a63ffefe949b12d32ec2344e845f7ff6dbffa0a0.torrent'
subgroup_id = 615
seed_name = '[GJ.Y] LV1 魔王与独居废勇者 / Lv1 Maou to One Room Yuusha - 12 (Baha 1920x1080 AVC AAC MP4)'
seed_status = 0

seed_obj = Seed(mikan_id, episode, seed_url, subgroup_id, seed_name, seed_status)
seed_dict = {'mikan_id': mikan_id, 'episode': episode, 'seed_url': seed_url, 'subgroup_id': subgroup_id, 'seed_name': seed_name, 'seed_status': seed_status}

timer_obj = timeit.Timer("Seed(3080, 12, '/Download/20230918/a63ffefe949b12d32ec2344e845f7ff6dbffa0a0.torrent', 516, '[GJ.Y] LV1 魔王与独居废勇者 / Lv1 Maou to One Room Yuusha - 12 (Baha 1920x1080 AVC AAC MP4)', 0)", setup="from __main__ import Seed")
timer_dict = timeit.Timer("{'mikan_id': 3080, 'episode': 12, 'seed_url': '/Download/20230918/a63ffefe949b12d32ec2344e845f7ff6dbffa0a0.torrent', 'subgroup_id': 516, 'seed_name': '[GJ.Y] LV1 魔王与独居废勇者 / Lv1 Maou to One Room Yuusha - 12 (Baha 1920x1080 AVC AAC MP4)', 'seed_status': 0}", setup="")

print("类对象占用的内存：{} 字节".format(sys.getsizeof(seed_obj)))
print("字典占用的内存：{} 字节".format(sys.getsizeof(seed_dict)))

print("对象创建耗时: {} 秒".format(timer_obj.timeit(number=1000)))
print("字典创建耗时: {} 秒".format(timer_dict.timeit(number=1000)))
