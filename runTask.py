import os
import sys
from lib.connect import m_DBconnector
from lib.spider import m_mikan
from lib.logManager import m_LogManager
from addAnimeTask import AddAnimeTask
from addqbTask import AddqbTask

logger = m_LogManager.getLogObj(sys.argv[0])

conn_info = dict(
    host = "10.112.5.25",
    port = "8081",
    username = "admin",
    password = "adminadmin",
)

m_addAnimeTask= AddAnimeTask(logger)
m_addqbTask = AddqbTask(conn_info,logger)

if __name__ == '__main__':
    m_addAnimeTask.deletAllTask()
    m_addAnimeTask.getAnimeTaskByMikanId(3060)
    torrentInfos = m_addqbTask.getTorrentInfo(m_addAnimeTask.animeTask)
    print(torrentInfos)
    m_addqbTask.addTorrents(torrentInfos, m_addAnimeTask.mikanIdToName(3060))
