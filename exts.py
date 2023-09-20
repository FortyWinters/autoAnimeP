import sys
from flask_sqlalchemy import SQLAlchemy
from lib.addAnimeTask import AddAnimeTask
from lib.addqbTask import AddqbTask
from lib.logManager import m_LogManager
from lib.config import m_config
from lib.spider import m_mikan

config = m_config
qb_info = config.get('QB')

db = SQLAlchemy()
logger = m_LogManager.getLogObj(sys.argv[0])
mikan = m_mikan
addqbTask = AddqbTask(qb_info, logger)
addAnimeTask= AddAnimeTask(logger)