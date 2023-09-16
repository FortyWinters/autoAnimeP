import requests
import urllib.request
from fake_useragent import UserAgent
from lxml import etree
from common import Anime, Seed, Subgroup
import ssl
import re
from logManager import LogManager
import sys

logger = LogManager(sys.argv[0]).getLogObj()

class Mikan:
    def __init__(self):
        self.url = "https://mikanani.me"
        self.ua = UserAgent()

    def request_html(self, url):
        try:
            headers = {'User-Agent': self.ua.random}
            res = requests.get(url=url, headers=headers, timeout=10)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            html_doc = etree.HTML(res.text)
        except Exception as e:
            logger.warning("[SPIDER]request_html failed, url: {}, error: {}".format(url, e))
            # print("[ERROR][SPIDER]request_html failed, url: {}, error: {}".format(url, e))
        else:
            logger.info("[SPIDER]request_html success, url: {}".format(url))
            # print("[INFO][SPIDER]request_html success, url: {}".format(url))
            return html_doc
        
    def download(self, url, path):
        ssl._create_default_https_context = ssl._create_unverified_context
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', self.ua.random)]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(url, path)
        except Exception as e:
            logger.warning("[SPIDER]download failed, url: {}, error: {}".format(url, e))
            # print("[ERROR][SPIDER]download failed, url: {}, error: {}".format(url, e))
            return False
        else:
            logger.info("[SPIDER]download success, url: {}".format(url))
            # print("[INFO][SPIDER]download success, url: {}".format(url))
            return True
    
    def get_anime_list(self):
        html_doc = self.request_html(self.url)
        if html_doc == None:
            logger.warning("[SPIDER]get_anime_list failed, request_html failed, url: {}".format(self.url))
            # print("[ERROR][SPIDER]get_anime_list failed, request_html failed, url: {}".format(self.url))
            return
        
        anime_list = []

        for info in html_doc.xpath('//div[@class="sk-bangumi"]'):
            update_day_ = info.xpath('.//@data-dayofweek')
            anime_info = info.xpath('.//li')
            for a in anime_info:
                anime_name_ = a.xpath('.//@title')[0]
                mikan_id_ = a.xpath('.//@data-bangumiid')[0]
                img_url_ = a.xpath('.//@data-src')
                
                anime_name = self.lxml_result_to_str(anime_name_)
                mikan_id = int(self.lxml_result_to_str(mikan_id_))
                img_url = self.lxml_result_to_str(img_url_)
                update_day = int(self.lxml_result_to_str(update_day_))

                if update_day == 7:   # movie
                    anime_type = 1
                    update_day = 0
                elif update_day == 8: # ova
                    anime_type = 2
                    update_day = 0
                elif update_day == 0: # update on sunday
                    anime_type = 0
                    update_day = 7
                else:
                    anime_type = 0

                subscribe_status = 0
                anime = Anime(anime_name, mikan_id, img_url, update_day, anime_type, subscribe_status)
                anime_list.append(anime)
        logger.info("[SPIDER]get_anime_list success, anime number: {}".format(len(anime_list)))
        # print("[INFO][SPIDER]get_anime_list success, anime number: {}".format(len(anime_list)))
        return anime_list

    def get_subgroup_list(self, mikan_id):
        url = "{}/Home/Bangumi/{}".format(self.url, mikan_id)
        html_doc = self.request_html(url)
        if html_doc == None:
            logger.warning("[SPIDER]get_subgroup_list failed, request_html failed, url: {}".format(self.url))
            # print("[ERROR][SPIDER]get_subgroup_list failed, request_html failed, url: {}".format(self.url))
            return
        
        subgroup_list = []

        subgroup_id_ = html_doc.xpath('//li[@class="leftbar-item"]/span/a/@data-anchor')
        subgroup_name_ = html_doc.xpath('//li[@class="leftbar-item"]/span/a/text()')
        
        for i in range(len(subgroup_name_)):
            subgroup_id = int(self.lxml_result_to_str(subgroup_id_[i])[1:])
            subgroup_name = self.lxml_result_to_str(subgroup_name_[i])

            subgroup = Subgroup(subgroup_id, subgroup_name)
            subgroup_list.append(subgroup)
        
        logger.info("[SPIDER]get_subgroup_list success, mikan_id: {}, subgroup number: {}".format(mikan_id, len(subgroup_list)))
        # print("[INFO][SPIDER]get_subgroup_list success, mikan_id: {}, subgroup number: {}".format(mikan_id, len(subgroup_list)))
        return subgroup_list
    
    def get_seed_list(self, mikan_id, subgroup_id):
        url = "{}/Home/ExpandEpisodeTable?bangumiId={}&subtitleGroupId={}&take=65".format(self.url, mikan_id, subgroup_id)
        html_doc = self.request_html(url)
        if html_doc == None:
            logger.warning("[SPIDER]get_seed_list failed, request_html failed, url: {}".format(self.url))
            # print("[ERROR][SPIDER]get_seed_list failed, request_html failed, url: {}".format(self.url))
            return
        
        seed_list = []

        tr_list = html_doc.xpath('//tbody/tr')
        for tr in tr_list:
            seed_url_ = tr.xpath('.//a[last()]/@href')
            seed_name_ = tr.xpath('.//a[@class="magnet-link-wrap"]/text()')

            seed_url = self.lxml_result_to_str(seed_url_)
            seed_name = self.lxml_result_to_str(seed_name_)

            if not self.if_1080(seed_name):
                continue

            episode_str = self.get_episode(seed_name)
            if episode_str == "null":
                continue

            episode = int(episode_str)
            seed = Seed(mikan_id, episode, seed_url, subgroup_id, seed_name)
            seed_list.append(seed)
        
        logger.info("[SPIDER]get_seed_list success, mikan_id: {}, subgroup_id: {}, seed number: {}".format(mikan_id, subgroup_id, len(seed_list)))
        # print("[INFO][SPIDER]get_seed_list success, mikan_id: {}, subgroup_id: {}, seed number: {}".format(mikan_id, subgroup_id, len(seed_list)))        
        return seed_list
    
    def download_img(self, img_url, path):
        url = "{}{}".format(self.url, img_url)
        img_name = img_url.split('/')[4]
        if not self.download(url, path + img_name):
            logger.warning("[SPIDER]download_img failed, download failed, img_url: {}, path: {}".format(img_url, path))
            # print("[ERROR][SPIDER]download_img failed, download failed, img_url: {}, path: {}".format(img_url, path))
            return False
        logger.info("[SPIDER]download_img success, img_url: {}, path: {}".format(img_url, path))
        # print("[INFO][SPIDER]download_img success, img_url: {}, path: {}".format(img_url, path))
        return True

    def download_seed(self, seed_url, path):
        url = "{}{}".format(self.url, seed_url)
        torrent_name = seed_url.split('/')[3]
        if not self.download(url, path + torrent_name):
            logger.warning("[SPIDER]download_seed failed, download failed, seed_url: {}, path: {}".format(seed_url, path))
            # print("[ERROR][SPIDER]download_seed failed, download failed, seed_url: {}, path: {}".format(seed_url, path))
            return False
        logger.info("[SPIDER]download_seed sucess, seed_url: {}, path: {}".format(seed_url, path))
        # print("[INFO][SPIDER]download_seed sucess, seed_url: {}, path: {}".format(seed_url, path))   
        return True

    def lxml_result_to_str(self, result):
        result_str = ''
        for a in result:
            result_str += str(a)
        return result_str

    def get_episode(self, seed_name):
        str_list = re.findall(r'\[\d{2}\]|\s\d{2}\s', seed_name)
        if len(str_list) == 0:
            return "null"
        episode_str = str_list[0][1:-1] 
        return episode_str

    def if_1080(self, seed_name):
        str_list = re.findall(r'1080p|x1080\s|\s1080\s', seed_name)
        if len(str_list) == 0:
            return False
        return True
        
if __name__ == '__main__':
    mikan = Mikan()
    # anime_list = mikan.get_anime_list()
    # subgroup_list = mikan.get_subgroup_list(3060)
    # seed_list = mikan.get_seed_list(3060, 611)

    # print(mikan.download_seed("/Download/20230913/dfe6eb7c5f780e90f74244a498949375c67143b0.torrent", "seed/"))
    # print(mikan.download_img("/images/Bangumi/202307/f94fdb7f.jpg", "static/img/anime_list"))