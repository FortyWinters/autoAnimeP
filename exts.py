import sys
from flask_sqlalchemy import SQLAlchemy
from lib.addAnimeTask import AddAnimeTask
from lib.addqbTask import AddqbTask
from lib.spider import m_mikan
from lib.logManager import m_LogManager

db = SQLAlchemy()
mikan = m_mikan
logger = m_LogManager.getLogObj(sys.argv[0])

conn_info = dict(
    host = "10.112.5.25",
    port = "8081",
    username = "admin",
    password = "adminadmin",
)

addqbTask = AddqbTask(conn_info, logger)
addAnimeTask= AddAnimeTask(logger)