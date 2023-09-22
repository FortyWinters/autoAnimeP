import sys
from flask_sqlalchemy import SQLAlchemy
from lib.logManager import m_LogManager
from lib.config import m_config
from lib.spider import m_mikan
from lib.addqbTask import m_addqbTask

db = SQLAlchemy()

config = m_config
logger = m_LogManager.getLogObj(sys.argv[0])
mikan = m_mikan
qb = m_addqbTask