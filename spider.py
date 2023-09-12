import requests
import urllib.request
from fake_useragent import UserAgent
from lxml import etree
from common import *
import ssl

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
        
def lxml_result_to_str(result):
    result_str = ''
    for a in result:
        result_str += str(a)
    return result_str
        
if __name__ == '__main__':
    mikan = Mikan()
    list = mikan.get_anime_list()

