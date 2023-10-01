import sys
import qbittorrentapi

class AddqbTask:
    def __init__(self, conn_info, logger, anime_config):
        self.conn_info = conn_info
        self.config = anime_config
        self.logger = logger
        self.qbt_client = self.connectqB()

    def connectqB(self):
        qbt_client = qbittorrentapi.Client(**self.conn_info)
        try:
             qbt_client.auth_log_in()
        except Exception as e:
            self.logger.error("[AddqbTask] Login failed.")
            sys.exit()
        return qbt_client
    
    # task_lists <- animeTask
    # animeTask : {mikan_id, {episode, seed_url}}
    def getTotalTorrentInfos(self, task_lists):
        total_torrent_infos = dict()
        for mikan_id, task in task_lists.items():
            total_torrent_infos[mikan_id] = self.getTorrentInfosByTask(mikan_id, task)
        return total_torrent_infos

    # task <- {episode, seed_url}
    def getTorrentInfosByTask(self, mikan_id, task):
        torrent_infos = dict()

        for episode,seed_url in task.items():
            torrent_info = dict()

            torrent_name = seed_url.split('/')[3]
            path = self.config['SEED'] + str(mikan_id) + '/' + torrent_name
            torrent_info['name']     = torrent_name
            torrent_info['path']     = path
    
            torrent_infos[episode] = torrent_info
        return torrent_infos

    def addTorrents(self, anime_name, torrent_infos):
        for _, torrent_info in torrent_infos.items():
            path = torrent_info['path']
            local_save_path = '/downloads/' + anime_name
            try:
                self.qbt_client.torrents_add(torrent_files=path,save_path=local_save_path)
            except Exception as e:
                self.logger.warning("[AddqbTask] Failed to add torrent seed:", torrent_info['name'])

    def pauseTorrent(self):
        # pause all torrents
        self.qbt_client.torrents.pause.all()