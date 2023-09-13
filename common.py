class Anime:
    def __init__(self, anime_name, mikan_id, img_url, update_day):
        self.anime_name = anime_name
        self.mikan_id   = mikan_id
        self.img_url    = img_url
        self.update_day = update_day

class Seed:
    def __init__(self, mikan_id, episode, seed_url, subgroup, seed_name):
        self.mikan_id  = mikan_id
        self.episode   = episode
        self.seed_url  = seed_url
        self.subgroup  = subgroup
        self.seed_name = seed_name

class Task:
    def __init__(self, mikan_id, episode, status, torrent_name):
        self.mikan_id     = mikan_id
        self.episode      = episode
        self.status       = status
        self.torrent_name = torrent_name