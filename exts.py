import sys
from flask_sqlalchemy import SQLAlchemy
from lib.spider import m_mikan
from lib.logManager import m_LogManager

mikan = m_mikan
logger = m_LogManager.getLogObj(sys.argv[0])
db = SQLAlchemy()