import sys
from flask_sqlalchemy import SQLAlchemy
from concurrent.futures import ThreadPoolExecutor
from lib.config import m_config
from lib.logManager import m_LogManager
from lib.addqbTask import m_addqbTask
from lib.spider import Mikan

config = m_config
logger = m_LogManager.getLogObj(sys.argv[0])
qb = m_addqbTask

db = SQLAlchemy()
executor = ThreadPoolExecutor(max_workers=config.get('SPIDER')['THREAD_POOL_SIZE_LIMIT'])
mikan = Mikan(logger, config.get('SPIDER'), executor)