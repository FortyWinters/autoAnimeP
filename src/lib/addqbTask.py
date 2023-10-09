import os
import sys
import qbittorrentapi
from datetime import timedelta

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
    # animeTask : {mikan_id, {episode, {torrent_name, path, subgroup_id}}}
    def getTotalTorrentInfos(self, task_lists):
        total_torrent_infos = dict()
        for mikan_id, task in task_lists.items():
            total_torrent_infos[mikan_id] = self.getTorrentInfosByTask(mikan_id, task)
        return total_torrent_infos

    # task <- {episode, [torrent_name, subgroupname]}
    def getTorrentInfosByTask(self, mikan_id, task):
        torrent_infos = dict()

        for episode, seed_info in task.items():
            torrent_info = dict()
            seed_url = seed_info[0]
            subgroup_id = seed_info[1]

            torrent_name = seed_url.split('/')[3]
            path = self.config['SEED'] + str(mikan_id) + '/' + torrent_name
            torrent_info['name']         = seed_url
            torrent_info['path']         = path
            torrent_info['subgroup_id'] = subgroup_id
    
            torrent_infos[episode] = torrent_info
        return torrent_infos

    def addTorrents(self, anime_name, torrent_infos):
        for _, torrent_info in torrent_infos.items():
            path = torrent_info['path']
            local_save_path = '/downloads/' + anime_name
            try:
                self.qbt_client.torrents_add(torrent_files=path,save_path=local_save_path)
            except Exception as e:
                self.logger.error("[AddqbTask] Failed to add torrent seed:", torrent_info['name'])

    def pauseTorrent(self):
        # pause all torrents
        self.qbt_client.torrents.pause.all()

    def get_torrent_web_info(self, torrent_name):
        torrent_hash = torrent_name.split('/')[3][:-8]
        torrent = self.qbt_client.torrents_info(hashes=torrent_hash)[0]

        # Name
        name = torrent["name"]

        # Size
        size = torrent["size"] / (1024 * 1024)
        if size > 1000:
            size_str = str(round(size / 1024, 2)) + ' GB'
        else:
            size_str = str(round(size, 2)) + ' MB'
        
        # State
        state = torrent["state"]

        # Done
        done = round(torrent["progress"] * 100, 2)
        done_str = str(done) + ' %'
        
        # Seeds
        seed = str(torrent["num_seeds"])
        
        # Peers
        peers = str(torrent["num_leechs"])
        
        # Download Speed
        download_speed = torrent["dlspeed"] / 1024
        if download_speed > 1000:
            download_speed_str = str(round(download_speed / 1024, 2)) + ' MBps'
        else:
            download_speed_str = str(round(download_speed, 2)) + ' KBps'

        # ETA
        eta_formatted = str(timedelta(seconds=torrent['eta']))

        torrent_web_info = dict(
            Name           = name,
            Size           = size_str,
            State          = state,
            Done           = done_str,
            Seeds          = seed,
            Peers          = peers,
            Download_speed = download_speed_str,
            ETA            = eta_formatted
        )
        return torrent_web_info
    
    def del_torrent(self, torrent_name):
        torrent_hash = torrent_name.split('/')[3][:-8]
        try:
            self.qbt_client.torrents_delete(hashes=torrent_hash, delete_files=True)
            self.logger.info("[AddqbTask][del_torrent] successfully delete torrent by torrent_name: {} ".format(torrent_name))
        except Exception as e:
            self.logger.error("[AddqbTask][del_torrent] failed to delete torrent by torrent_name: {}".format(torrent_name))
    
    def get_completed_torrent_list(self):
        try:
            completed_torrent_list = self.qbt_client.torrents_info(filter='completed')
            self.logger.info("[AddqbTask][get_completed_torrent_list] successfully get completed torrent list")
        except Exception as e:
            self.logger.warning("[AddqbTask][get_completed_torrent_list] failed to get completed torrent list, error: {}".format(e))
        else:
            return completed_torrent_list
        
    def rename_torrent_file(self, anime_name, torrent_infos):
        for episode, torrent_info in torrent_infos.items():
            torrent_name = torrent_info['name']
            torrent_hash = torrent_name.split('/')[3][:-8]
            subgroup_name = torrent_info['subgroupname']
            # torrent = self.qbt_client.torrents_info(hashes=torrent_hash)[0]
            
            file = self.qbt_client.torrents_files(torrent_hash)
            self.logger.info("[AddqbTask][get_completed_torrent_list] {}".format(file))
            file_extension = os.path.splitext(file[0]['name'])[1]
            new_name = anime_name + ' - ' + str(episode) + ' - ' + subgroup_name + file_extension

            try:
                self.qbt_client.torrents_rename_file(torrent_hash=torrent_hash, file_id=0, new_file_name=new_name)
            except Exception as e:
                self.logger.warning("[AddqbTask] Failed to rename torrent file with new name: {} ".format(new_name))
            self.logger.info("[AddqbTask] successfully rename torrent file with new name: {} ".format(new_name))
    
    def pause_qb_task(self, torrent_name):
        torrent_hash = torrent_name.split('/')[3][:-8]

        try:
            self.qbt_client.torrents_pause(torrent_hashes=torrent_hash)
        except Exception as e:
            self.logger.error("[AddqbTask] Failed to pause torrent: {} ".format(torrent_name))
        self.logger.info("[AddqbTask] Successfully pause torrent: {} ".format(torrent_name))
    
    def resume_qb_task(self, torrent_name):
        torrent_hash = torrent_name.split('/')[3][:-8]

        try:
            self.qbt_client.torrents_resume(torrent_hashes=torrent_hash)
        except Exception as e:
            self.logger.error("[AddqbTask] Failed to resume torrent: {} ".format(torrent_name))
        self.logger.info("[AddqbTask] Successfully resume torrent: {} ".format(torrent_name))
    
    def pause_seeding(self, torrent_name):
        torrent_hash = torrent_name.split('/')[3][:-8]
        try:
            self.qbt_client.torrents_set_share_limits(torrent_hashes=torrent_hash, 
                                                      ratio_limit=-2, 
                                                      seeding_time_limit=0)
        except Exception as e:
            self.logger.error("[AddqbTask] Failed to pause seeding for torrent: {}.".format(torrent_name))
        self.logger.info("[AddqbTask] Successfully pause seeding for torrent: {}.".format(torrent_name))

    def pause_seeding_all(self):
        torrents = self.qbt_client.torrents_info()
        for torrent in torrents:
            torrent_name = torrent['name']
            torrent_hash = torrent['hash']
            try:
                self.qbt_client.torrents_set_share_limits(torrent_hashes=torrent_hash, 
                                                        ratio_limit=-2, 
                                                        seeding_time_limit=0)
            except Exception as e:
                self.logger.error("[AddqbTask] Failed to pause seeding for torrent: {}.".format(torrent_name))
            self.logger.info("[AddqbTask] Successfully pause seeding for torrent: {}.".format(torrent_name))