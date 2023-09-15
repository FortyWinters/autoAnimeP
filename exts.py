import sys
from logManager import LogManager
from flask_sqlalchemy import SQLAlchemy
from spider import Mikan

logger = LogManager(sys.argv[0]).getLogObj()
db = SQLAlchemy()
mikan = Mikan()