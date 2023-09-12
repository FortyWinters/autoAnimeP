import re
import ssl
import requests
import urllib.request
from fake_useragent import UserAgent
import paramiko

QB_IP = "10.129.47.21"
QB_USERNAME = "root"
QB_PASSWORD = "aa987b6d9aceedce111b4be891dbb3d2"
QB_PATH = "/tmp/mountd/disk1_part1/qBittorrent/torrentFiles/"

SEED_PATH = "/home/csy/autoAnime/seed/"



class Mikan:
    def __init__(self, search_list):
        self.url = "https://mikanani.me"
        self.ua = UserAgent()
        self.search_list = search_list
    
    def get_url(self, search_str):
        search_str_list = search_str.split('+')
        search_url = ""
        for word in search_str_list:
            if '\u4e00' <= word <= '\u9fff':
                url_encoded = urllib.parse.quote(word)
                search_url += url_encoded + '+'
            else:
                search_url += word + '+'
        return search_url[:-1]

    def get_page(self, search_url):
        search_url = self.url + "/Home/Search?searchstr=" + search_url
        headers = {'User-Agent': self.ua.random}
        res = requests.get(url=search_url, headers=headers).text
        return res
    
    def get_seed_list(self, html, search_str):
        seed_list = re.findall(r'/Download.*torrent', html)
        if len(seed_list) == 0:
            print("未发现种子QAQ (" + search_str + ")")
            return
        return seed_list

    def download_seed(self, seed_url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', self.ua.random)]
        urllib.request.install_opener(opener)
        try:
            #urllib.request.urlretrieve(self.url + seed_url, 'seed/' + seed_url.replace('/', '_')[1:] + '.torrent')
            urllib.request.urlretrieve(self.url + seed_url, 'seed/' + seed_url.replace('/', '_')[1:])
            print("种子下载成功! (" + seed_url + ")")
            return True
        except Exception as e:
            print(e)
            print("种子下载失败QAQ (" + seed_url + ")")
            return False
            
    def run_with_sftp(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            t = paramiko.Transport((QB_IP, 22))
            t.banner_timeout = 10
            t.connect(username=QB_USERNAME, password=QB_PASSWORD)
            sftp = paramiko.SFTPClient.from_transport(t)
            print("sftp连接建立成功")
        except Exception as e:
            print("sftp连接建立失败")
            print(e)
            return
        
        print("搜索开始\n")
        for search_str in self.search_list:
            search_url = self.get_url(search_str)
            print("搜索[" + search_str + ']')
            html = self.get_page(search_url)
            seed_url_list = self.get_seed_list(html, search_str)

            for seed_url in seed_url_list:
                res = self.download_seed(seed_url)
                if not res:
                    continue

                local = SEED_PATH + seed_url.replace('/', '_')[1:]
                server = QB_PATH + seed_url.replace('/', '_')[1:]

                try:
                    sftp.put(local, server)
                    print("种子上传成功")
                except Exception as e:
                    print("种子上传失败")
                    print(e)
                    print("\n")
            
            print('\n')

        t.close()
        print("sftp连接断开")
        
if __name__ == '__main__':
    search_list = [
        "无职转生+1080p+二",
        "死神+诀别+Lilith+1080p"
    ]
    mikan = Mikan(search_list)
    mikan.run_with_sftp()