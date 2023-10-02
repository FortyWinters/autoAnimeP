import sys
from flask_sqlalchemy import SQLAlchemy
from concurrent.futures import ThreadPoolExecutor
from lib.config import m_config
from lib.logManager import m_LogManager
from lib.addqbTask import AddqbTask
from lib.spider import Mikan
from lib.connect import DBconnect

config = m_config
logger = m_LogManager.getLogObj(sys.argv[0])

db = SQLAlchemy()
qb = AddqbTask(config.get('QB'),logger, config.get('DOWNLOAD'))
m_DBconnector = DBconnect(config.get('MySQL'))
executor = ThreadPoolExecutor(max_workers=config.get('SPIDER')['THREAD_POOL_SIZE_LIMIT'])
mikan = Mikan(logger, config.get('SPIDER'), executor)