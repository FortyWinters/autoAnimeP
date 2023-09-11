import qbittorrentapi

class qBconnector:
    def __init__(self, conn_info):
        self.conn_info = conn_info
        self.qbt_client = self.connect()

    def connect(self):
        qbt_client = qbittorrentapi.Client(**self.conn_info)
        try:
             qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)
        return qbt_client

    def putTorrent(self):
        # Todo: read torrent from db

        self.qbt_client.torrents_add(torrent_files='/path/to/torrent/1.torrent',save_path='/downloads')

    def pauseTorrent(self):
        self.qbt_client.torrents.pause.all()

if __name__ == '__main__':
    
    conn_info = dict(
        host = "10.112.5.25",
        port = "8081",
        username = "admin",
        password = "adminadmin",
    )

    qb = qBconnector(conn_info)

# instantiate a Client using the appropriate WebUI configuration
# conn_info = dict(
#     host="10.112.5.25",
#     port=8081,
#     username="admin",
#     password="adminadmin",
# )
# qbt_client = qbittorrentapi.Client(**conn_info)

# the Client will automatically acquire/maintain a logged-in state
# in line with any request. therefore, this is not strictly necessary;
# however, you may want to test the provided login credentials.
# try:
#     qbt_client.auth_log_in()
# except qbittorrentapi.LoginFailed as e:
#     print(e)
# qbt_client.torrents_add(torrent_files='/Users/haisongbi/Downloads/1.torrent',save_path='/downloads')

# or use a context manager:
# with qbittorrentapi.Client(**conn_info) as qbt_client:
#     if qbt_client.torrents_add(urls="...") != "Ok.":
#         raise Exception("Failed to add torrent.")

# display qBittorrent info
# print(f"qBittorrent: {qbt_client.app.version}")
# print(f"qBittorrent Web API: {qbt_client.app.web_api_version}")
# for k, v in qbt_client.app.build_info.items():
#     print(f"{k}: {v}")

# # retrieve and show all torrents
# for torrent in qbt_client.torrents_info():
#     print(f"{torrent.hash[-6:]}: {torrent.name} ({torrent.state})")

# # pause all torrents
# qbt_client.torrents.pause.all()

# if the Client will not be long-lived or many Clients may be created
# in a relatively short amount of time, be sure to log out:
# qbt_client.auth_log_out()