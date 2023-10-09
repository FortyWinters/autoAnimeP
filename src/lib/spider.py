import re
import ssl
import requests
import urllib.request
from lxml import etree
from fake_useragent import UserAgent
from concurrent.futures import wait, ALL_COMPLETED
from .common import Anime, Seed, Subgroup

class Mikan:
    def __init__(self, logger, config, executor):
        self.url = config['URL']
        self.ua = UserAgent()
        self.logger = logger
        self.executor = executor
        self.seed_list = []
        self.seed_list_download_sucess = []
        self.seed_list_download_failed = []
        self.img_list_download = []

    def request_html(self, url):
        try:
            headers = {'User-Agent': self.ua.random}
            res = requests.get(url=url, headers=headers, timeout=5)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            html_doc = etree.HTML(res.text)
        except Exception as e:
            self.logger.warning("[SPIDER] request_html failed, url: {}, error: {}".format(url, e))
        else:
            self.logger.info("[SPIDER] request_html success, url: {}".format(url))
            return html_doc
        
    def download(self, url, path):
        ssl._create_default_https_context = ssl._create_unverified_context
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', self.ua.random)]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(url, path)
        except Exception as e:
            self.logger.warning("[SPIDER] download failed, url: {}, error: {}".format(url, e))
            return False
        else:
            self.logger.info("[SPIDER] download success, url: {}".format(url))
            return True
    
    def get_anime_list(self):
        html_doc = self.request_html(self.url)
        if html_doc == None:
            self.logger.warning("[SPIDER] get_anime_list failed, request_html failed, url: {}".format(self.url))
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
                    update_day = 8
                elif update_day == 8: # ova
                    anime_type = 2
                    update_day = 8
                elif update_day == 0: # update on sunday
                    anime_type = 0
                    update_day = 7
                else:
                    anime_type = 0

                subscribe_status = 0
                anime = Anime(anime_name, mikan_id, img_url, update_day, anime_type, subscribe_status)
                anime_list.append(anime)
        self.logger.info("[SPIDER] get_anime_list success, anime number: {}".format(len(anime_list)))
        return anime_list

    def get_subgroup_list(self, mikan_id):
        url = "{}/Home/Bangumi/{}".format(self.url, mikan_id)
        html_doc = self.request_html(url)
        if html_doc == None:
            self.logger.warning("[SPIDER] get_subgroup_list failed, request_html failed, url: {}".format(self.url))
            return
        
        subgroup_list = []

        subgroup_id_ = html_doc.xpath('//li[@class="leftbar-item"]/span/a/@data-anchor')
        subgroup_name_ = html_doc.xpath('//li[@class="leftbar-item"]/span/a/text()')
        
        for i in range(len(subgroup_name_)):
            subgroup_id = int(self.lxml_result_to_str(subgroup_id_[i])[1:])
            subgroup_name = self.lxml_result_to_str(subgroup_name_[i])

            subgroup = Subgroup(subgroup_id, subgroup_name)
            subgroup_list.append(subgroup)
        
        self.logger.info("[SPIDER] get_subgroup_list success, mikan_id: {}, subgroup number: {}".format(mikan_id, len(subgroup_list)))
        return subgroup_list
    
    def get_seed_list(self, mikan_id, subgroup_id, anime_type):
        url = "{}/Home/ExpandEpisodeTable?bangumiId={}&subtitleGroupId={}&take=65".format(self.url, mikan_id, subgroup_id)
        html_doc = self.request_html(url)
        if html_doc == None:
            self.logger.warning("[SPIDER] get_seed_list failed, request_html failed, url: {}".format(self.url))
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

            if anime_type == '0':
                episode_str = self.get_episode(seed_name)
                if episode_str == "null":
                    continue
            else:
                episode_str = "01"

            episode = int(episode_str)
            seed_status = 0
            seed = Seed(mikan_id, episode, seed_url, subgroup_id, seed_name, seed_status)
            seed_list.append(seed)
        
        self.logger.info("[SPIDER] get_seed_list success, mikan_id: {}, subgroup_id: {}, anime_type: {}, seed number: {}".format(mikan_id, subgroup_id, anime_type, len(seed_list)))   
        return seed_list
    
    # mikan.download_img("/images/Bangumi/202307/f94fdb7f.jpg", "static/img/anime_list")
    def download_img(self, img_url, path):
        url = "{}{}".format(self.url, img_url)
        img_name = img_url.split('/')[4]
        if not self.download(url, path + img_name):
            self.logger.warning("[SPIDER] download_img failed, download failed, img_url: {}, path: {}".format(img_url, path))
            return False
        self.logger.info("[SPIDER] download_img success, img_url: {}, path: {}".format(img_url, path))
        return True

    # mikan.download_seed("/Download/20230913/dfe6eb7c5f780e90f74244a498949375c67143b0.torrent", "seed/")
    def download_seed(self, seed_url, path):
        url = "{}{}".format(self.url, seed_url)
        torrent_name = seed_url.split('/')[3]
        if not self.download(url, path + torrent_name):
            self.logger.warning("[SPIDER] download_seed failed, download failed, seed_url: {}, path: {}".format(seed_url, path))
            return False
        self.logger.info("[SPIDER] download_seed sucess, seed_url: {}, path: {}".format(seed_url, path))
        return True

    def lxml_result_to_str(self, result):
        result_str = ''
        for a in result:
            result_str += str(a)
        return result_str

    def get_episode(self, seed_name):
        # 排除掉了合集
        str_list = re.findall(r'\d{2}-\d{2}', seed_name)
        if len(str_list) != 0:
            return "null"

        str_list = re.findall(r'\[\d{2}\]|\s\d{2}\s', seed_name)
        if len(str_list) == 0:
            str_list = re.findall(r'\[第\d+话\]', seed_name)
            if len(str_list) == 0:
                return "null"
            else:
                return str_list[0][2:-2]
        episode_str = str_list[0][1:-1] 
        return episode_str

    def if_1080(self, seed_name):
        str_list = re.findall(r'1080', seed_name)
        if len(str_list) == 0:
            return False
        return True
    
    def get_seed_list_thread(self, args):        
        mikan_id, subgroup_id, anime_type = args
        try:
            seed_list = self.get_seed_list(mikan_id, subgroup_id, anime_type)
        except Exception as e:
            self.logger.warning("[SPIDER] get_seed_list_thread failed, mikan_id: {}, subgroup_id: {}, error: {}".format(mikan_id, subgroup_id, e))
        else:
            for s in seed_list:
                self.seed_list.append(s)
    
    def get_seed_list_task(self, mikan_id, subgroup_list, anime_type):
        self.seed_list = []
        task_list = []
        for sub in subgroup_list:
            subgroup_id = sub.subgroup_id
            task = self.executor.submit(self.get_seed_list_thread, (mikan_id, subgroup_id, anime_type))
            task_list.append(task)
        wait(task_list, return_when=ALL_COMPLETED)
        return self.seed_list
    
    def download_seed_thread(self, args):
        seed = args
        seed_url = seed['seed_url']
        path = seed['path']
        try:
            self.download_seed(seed_url, path)
        except Exception as e:
            self.logger.warning("[SPIDER] download_seed_thread failed, seed_url: {}, path: {}, error: {}".format(seed_url, path, e))
            self.seed_list_download_failed.append(seed)
        else:
            self.seed_list_download_sucess.append(seed)
 
    def download_seed_task(self, seed_list):
        self.seed_list_download_sucess = []
        self.seed_list_download_failed = []
        task_list = []
        for seed in seed_list:
            task = self.executor.submit(self.download_seed_thread, seed)
            task_list.append(task)
        wait(task_list, return_when=ALL_COMPLETED)
        return self.seed_list_download_sucess
    
    def download_img_thread(self, args):
        img = args
        img_url = img['img_url']
        path = img['path']
        try:
            self.download_img(img_url, path)
        except Exception as e:
            self.logger.warning("[SPIDER] download_img_thread failed, img_url: {}, path: {}".format(img_url, path))
        else:
            self.img_list_download.append(img)
    
    def download_img_task(self, img_list):
        self.img_list_download =  []
        task_list = []
        for img in img_list:
            task = self.executor.submit(self.download_img_thread, img)
            task_list.append(task)
        wait(task_list, return_when=ALL_COMPLETED)
        return self.img_list_download
    
    def get_anime_list_by_conditon(self, year, broadcast_season):
        if broadcast_season == 1:
            seasonStr = '%E6%98%A5'
        elif broadcast_season == 2:
            seasonStr ='%E5%A4%8F'
        elif broadcast_season == 3:
            seasonStr = '%E7%A7%8B'
        elif broadcast_season == 4:
            seasonStr = '%E5%86%AC'
        else:
            self.logger.warning("[SPIDER] get_anime_list_by_conditon failed, year: {}, broadcast_season: {}".format(year, broadcast_season))
            return
        
        url = "{}/Home/BangumiCoverFlowByDayOfWeek?year={}&seasonStr={}".format(self.url, year, seasonStr)
        html_doc = self.request_html(url)
        if html_doc == None:
            self.logger.warning("[SPIDER] get_anime_list failed, request_html failed, url: {}".format(self.url))
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
                    update_day = 8
                elif update_day == 8: # ova
                    anime_type = 2
                    update_day = 8
                elif update_day == 0: # update on sunday
                    anime_type = 0
                    update_day = 7
                else:
                    anime_type = 0

                subscribe_status = 0
                anime = Anime(anime_name, mikan_id, img_url, update_day, anime_type, subscribe_status)
                anime_list.append(anime)
        self.logger.info("[SPIDER] get_anime_list success, anime number: {}".format(len(anime_list)))
        return anime_list