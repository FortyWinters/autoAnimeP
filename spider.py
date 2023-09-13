import requests
import urllib.request
from fake_useragent import UserAgent
from lxml import etree
from common import Anime, Seed
import ssl
import re

class Mikan:
    def __init__(self):
        self.url = "https://mikanani.me"
        self.ua = UserAgent()

    def get_html(self, url):
        try:
            headers = {'User-Agent': self.ua.random}
            res = requests.get(url=url, headers=headers, timeout=10)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            return res.text
        except Exception as e:
            print(e)
    
    def get_anime_list(self):
        html = self.get_html(self.url)
        html_doc = etree.HTML(html)

        anime_list = []

        for info in html_doc.xpath('//div[@class="sk-bangumi"]'):
            update_day_ = info.xpath('.//@data-dayofweek')
            anime_info = info.xpath('.//li')
            for a in anime_info:
                anime_name_ = a.xpath('.//@title')[0]
                mikan_id_ = a.xpath('.//@data-bangumiid')[0]
                img_url_ = a.xpath('.//@data-src')
                
                anime_name = lxml_result_to_str(anime_name_)
                mikan_id = int(lxml_result_to_str(mikan_id_))
                img_url = lxml_result_to_str(img_url_)
                update_day = int(lxml_result_to_str(update_day_))
                if update_day == 7:
                    update_day = 9
                if update_day == 0:
                    update_day = 7 

                anime = Anime(anime_name, mikan_id, img_url, update_day)

                anime_list.append(anime)
        return anime_list
    
    def download(self, url, path):
        ssl._create_default_https_context = ssl._create_unverified_context
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', self.ua.random)]
        urllib.request.install_opener(opener)
        try:
            urllib.request.urlretrieve(url, path)
            print("下载成功! (" + url + ")")
            return True
        except Exception as e:
            print(e)
            print("下载失败QAQ (" + url + ")")
            return False
    
    def get_img(self, img_url, path):
        url = self.url + img_url
        img_name = img_url.split('/')[4]
        self.download(url, path + '/' + img_name)

    def get_seed_list(self, mikan_id):
        url = self.url + "/Home/Bangumi/" + str(mikan_id)
        html = self.get_html(url)
        html_doc = etree.HTML(html)
        
        subgroup_list = html_doc.xpath('//div[@class="central-container"]/div[@class="subgroup-text"]/a[@target="_blank"]/text()')
        table_list = html_doc.xpath('//div[@class="central-container"]/table')

        seed_list = []

        for i in range(len(subgroup_list)): 
            seed_name_list = table_list[i].xpath('.//a[@class="magnet-link-wrap"]/text()')
            seed_url_list = table_list[i].xpath('.//a[last()]/@href')

            subgroup = lxml_result_to_str(subgroup_list[i])
            
            for j in range(len(seed_name_list)):
                seed_name = lxml_result_to_str(seed_name_list[j])

                if not if_1080(seed_name):
                    continue

                episode_str = get_episode(seed_name)
                if episode_str == "null":
                    continue

                episode = int(episode_str)
                seed_url = lxml_result_to_str(seed_url_list[j])

                seed = Seed(mikan_id, episode, seed_url, subgroup, seed_name)
                seed_list.append(seed)
        
        return seed_list
            
def lxml_result_to_str(result):
    result_str = ''
    for a in result:
        result_str += str(a)
    return result_str

def get_episode(seed_name):
    str_list = re.findall(r'\[\d{1,2}\]|\s\d{1,2}\s', seed_name)
    if len(str_list) == 0:
        return "null"
    episode_str = str_list[0][1:-1] 
    return episode_str

def if_1080(seed_name):
    str_list = re.findall(r'1080p|x1080\s|\s1080\s', seed_name)
    if len(str_list) == 0:
        return False
    return True

        
if __name__ == '__main__':
    mikan = Mikan()
    list = mikan.get_anime_list()
    print(list[0].anime_name)
    print(list[0].mikan_id)
    seed_list = mikan.get_seed_list(list[0].mikan_id)
    for s in seed_list:
        print(s.seed_name)
        print(s.subgroup)
        print(s.episode)
        print(s.seed_url)

