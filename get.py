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
        search_str_list = search_str.split('-')
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
    
    def get_seed(self, html, search_str):
        seed_list = re.findall(r'/Download.*torrent', html)
        if len(seed_list) == 0:
            print("未发现种子QAQ (" + search_str + ")")
            return
        seed_url = self.url + seed_list[0]
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', self.ua.random)]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(seed_url, 'seed/' + urllib.parse.quote(search_str) + '.torrent')
        print("种子下载成功! (" + search_str + ")")

    def sftp_upload(self, search_str):
        try:
            t = paramiko.Transport((QB_IP, 22))
            t.banner_timeout = 10
            t.connect(username=QB_USERNAME, password=QB_PASSWORD)
            sftp = paramiko.SFTPClient.from_transport(t)
            local = SEED_PATH + urllib.parse.quote(search_str) + ".torrent"
            server = QB_PATH + urllib.parse.quote(search_str) + ".torrent"
            sftp.put(local, server)
            t.close()
            print("种子上传成功 (" + search_str +")\n")
        except Exception as e:
            print("种子上传失败 (" + search_str +")")
            print(e)
            print("\n")
            
    # 不用了
    def run(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        print("搜索开始\n")
        for search_str in self.search_list:
            search_url = self.get_url(search_str)
            html = self.get_page(search_url)
            self.get_seed(html, search_str)
            self.sftp_upload(search_str)
                
        print("搜索结束")

    def run_with_sftp(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        
        t = paramiko.Transport((QB_IP, 22))
        t.banner_timeout = 10
        t.connect(username=QB_USERNAME, password=QB_PASSWORD)
        try:
            sftp = paramiko.SFTPClient.from_transport(t)
            print("sftp连接建立成功")
        except Exception as e:
            print("sftp连接建立失败")
            print(e)
            return
        
        print("搜索开始\n")
        for search_str in self.search_list:
            search_url = self.get_url(search_str)
            html = self.get_page(search_url)
            self.get_seed(html, search_str)
            local = SEED_PATH + urllib.parse.quote(search_str) + ".torrent"
            server = QB_PATH + urllib.parse.quote(search_str) + ".torrent"
            try:
                sftp.put(local, server)
                print("种子上传成功 (" + search_str +")\n")
            except Exception as e:
                print("种子上传失败 (" + search_str +")")
                print(e)
                print("\n")
        t.close()
        print("sftp连接断开")
        
if __name__ == '__main__':
    anime_name = "无职转生-s2-1080p-Baha-0"
    search_list = []
    for i in range(12):
        search_list.append(anime_name + str(i + 1))
    
    mikan = Mikan(search_list)
    mikan.run_with_sftp()