import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from concurrent.futures import ThreadPoolExecutor
from lib.config import m_config
from lib.logManager import m_LogManager
from lib.addqbTask import AddqbTask
from lib.spider import Mikan
from lib.connect import DBconnect

def get_broadcast_map():
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    broadcast_map = dict()
    broadcast_map[2013] = [3]
    for year in range(2014, current_year):
        broadcast_map[year] = [4, 1, 2, 3]

    if current_month > 0 and current_month < 3:
        season_list = [4]
    elif current_month >= 3 and current_month < 6:
        season_list = [4, 1]
    elif current_month >= 6 and current_month < 9:
        season_list = [4, 1, 2]
    else:
        season_list = [4, 1, 2, 3]
    broadcast_map[current_year] = season_list

    return broadcast_map

config = m_config
logger = m_LogManager.getLogObj(sys.argv[0])

db = SQLAlchemy()
qb = AddqbTask(config.get('QB'),logger, config.get('DOWNLOAD'))
m_DBconnector = DBconnect(config.get('MySQL'))
executor = ThreadPoolExecutor(max_workers=config.get('SPIDER')['THREAD_POOL_SIZE_LIMIT'])
mikan = Mikan(logger, config.get('SPIDER'), executor)
broadcast_map = get_broadcast_map()