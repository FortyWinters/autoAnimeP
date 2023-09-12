import requests
import urllib.request
from fake_useragent import UserAgent
from lxml import etree
from common import *

class Mikan:
    def __init__(self):
        self.url = "https://mikanani.me"
        self.ua = UserAgent()

    def get_html(self):
        try:
            headers = {'User-Agent': self.ua.random}
            res = requests.get(url=self.url, headers=headers, timeout=10)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            return res.text
        except Exception as e:
            print(e)
    
    def get_anime_list(self):
        html = self.get_html()
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
    


def lxml_result_to_str(result):
    result_str = ''
    for a in result:
        result_str += str(a)
    return result_str
        
if __name__ == '__main__':
    mikan = Mikan()
    list = mikan.get_anime_list()
    for a in list:
        print(a.anime_name)
        print(a.mikan_id)
        print(a.img_url)
        print(a.update_day)
    
