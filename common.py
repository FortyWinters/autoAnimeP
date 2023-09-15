class Anime:
    def __init__(self, anime_name, mikan_id, img_url, update_day, anime_type, subscribe_status):
        self.anime_name       = anime_name
        self.mikan_id         = mikan_id
        self.img_url          = img_url
        self.update_day       = update_day
        self.anime_type       = anime_type
        self.subscribe_status = subscribe_status

class Seed:
    def __init__(self, mikan_id, episode, seed_url, subgroup_id, seed_name):
        self.mikan_id     = mikan_id
        self.episode      = episode
        self.seed_url     = seed_url
        self.subgroup_id  = subgroup_id
        self.seed_name    = seed_name

class Task:
    def __init__(self, mikan_id, episode, status, torrent_name):
        self.mikan_id     = mikan_id
        self.episode      = episode
        self.status       = status
        self.torrent_name = torrent_name

class Subgroup:
    def __init__(self, subgroup_id, subgroup_name):
        self.subgroup_id   = subgroup_id
        self.subgroup_name = subgroup_name