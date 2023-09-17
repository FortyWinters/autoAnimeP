import os
import sys
import qbittorrentapi
from lib.logManager import m_LogManager

class AddqbTask:
    def __init__(self, conn_info, logger):
        self.conn_info = conn_info
        self.qbt_client = self.connectqB()
        self.logger = logger

    def connectqB(self):
        qbt_client = qbittorrentapi.Client(**self.conn_info)
        try:
             qbt_client.auth_log_in()
        except Exception as e:
            print("Login failed .")
            sys.exit()
        return qbt_client
    
    def getTorrentInfo(self, task_lists):
        # Todo: read torrent from db
        torrentInfos = dict()

        for mikan_id, episode_info in task_lists.items():
            for episode, seed_url in episode_info.items():
                torrentInfo = dict()
        
                torrent_name = seed_url.split('/')[3]
                path = "seed/" + str(mikan_id) + '/' + torrent_name
                torrentInfo['name']     = torrent_name
                torrentInfo['episode']  = episode
                torrentInfo['path']     = path
                
                torrentInfos[episode] = torrentInfo
        
        # print(torrentInfos)
        return torrentInfos

    def addTorrents(self, torrentInfos, Anime_name):
        for _, torrentInfo in torrentInfos.items():
            path = torrentInfo['path']
            savePath = '/downloads/' + Anime_name
            try:
                self.qbt_client.torrents_add(torrent_files=path,save_path=savePath)
            except Exception as e:
                logger.warning("Failed to add torrent seed:", torrentInfo['name'])

    def pauseTorrent(self):
        # pause all torrents
        self.qbt_client.torrents.pause.all()
    
    def run(self):
        self.addTorrents()

conn_info = dict(
    host = "10.112.5.25",
    port = "8081",
    username = "admin",
    password = "adminadmin",
)

logger = m_LogManager.getLogObj(sys.argv[0])
m_addqbTask = AddqbTask(conn_info, logger)



# m_qBconnector.run()
# m_qBconnector.getTorrentInfo()

# display qBittorrent info
# print(f"qBittorrent: {qbt_client.app.version}")
# print(f"qBittorrent Web API: {qbt_client.app.web_api_version}")
# for k, v in qbt_client.app.build_info.items():
#     print(f"{k}: {v}")

# # retrieve and show all torrents
# for torrent in qbt_client.torrents_info():
#     print(f"{torrent.hash[-6:]}: {torrent.name} ({torrent.state})")

# if the Client will not be long-lived or many Clients may be created
# in a relatively short amount of time, be sure to log out:
# qbt_client.auth_log_out()