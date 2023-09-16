import sys
from flask_sqlalchemy import SQLAlchemy
from spider import Mikan
from logManager import m_LogManager

logger = m_LogManager.getLogObj(sys.argv[0])
db = SQLAlchemy()
mikan = Mikan()