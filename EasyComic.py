import qbittorrentapi
import sys

class qBconnector:
    def __init__(self, conn_info):
        self.conn_info = conn_info
        self.qbt_client = self.connectqB()

    def connectqB(self):
        qbt_client = qbittorrentapi.Client(**self.conn_info)
        try:
             qbt_client.auth_log_in()
        except Exception as e:
            print("Login failed .")
            sys.exit()
        return qbt_client

    def getTorrentInfo(self):
        # Todo: read torrent from db
        torrentInfo = dict(
            path = '/path/to/torrent/1.torrent',
            name = 'testName_2',
            episode = 1,
        )
        return torrentInfo

    def addTorrent(self):
        torrentInfo = self.getTorrentInfo()
        path = torrentInfo['path']
        savePath = '/downloads/' + torrentInfo['name']
        try:
            self.qbt_client.torrents_add(torrent_files=path,save_path=savePath)
        except Exception as e:
            print("Failed to add torrent seed:", torrentInfo['name'])

    def pauseTorrent(self):
        # pause all torrents
        self.qbt_client.torrents.pause.all()
    
    def run(self):
        self.addTorrent()

if __name__ == '__main__':
    conn_info = dict(
        host = "10.112.5.25",
        port = "8081",
        username = "admin",
        password = "adminadmin",
    )
    qBconnector(conn_info).run()

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