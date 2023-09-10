import re
import ssl
import requests
import urllib.request
from fake_useragent import UserAgent
import paramiko

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
            print("未发现种子QAQ (" + search_str + ")\n")
            return
        seed_url = self.url + seed_list[0]
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', self.ua.random)]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(seed_url, 'seed/' + urllib.parse.quote(search_str) + '.torrent')
        print("种子下载成功! (" + search_str + ")\n")

    def sftp_upload(self, search_str):
        try:
            t = paramiko.Transport(("10.129.47.21", 22))
            t.banner_timeout = 10
            t.connect(username="root", password="aa987b6d9aceedce111b4be891dbb3d2")
            sftp = paramiko.SFTPClient.from_transport(t)
            local = "/home/csy/autoAnime/seed/" + urllib.parse.quote(search_str) + ".torrent"
            server = "/tmp/mountd/disk1_part1/qBittorrent/torrentFiles/" + urllib.parse.quote(search_str) + ".torrent"
            sftp.put(local, server)
            t.close()
            return True
        except Exception as e:
            print(e)
        return False


    def run(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        print("搜索开始\n")
        for search_str in self.search_list:
            search_url = self.get_url(search_str)
            html = self.get_page(search_url)
            self.get_seed(html, search_str)
            res = self.sftp_upload(search_str)
            if not res:
                print("种子上传失败 (" + search_str +")\n")
            else:
                print("种子上传成功 (" + search_str +")\n")
        print("搜索结束")

if __name__ == '__main__':
    search_list = [
        "无职转生-s2-1080p-奶茶屋-4",
        "无职转生-s2-1080p-奶茶屋-15",
        "无职转生-s2-1080p-奶茶屋-6",
        "无职转生-s2-1080p-奶茶屋-7",
    ]
    mikan = Mikan(search_list)
    mikan.run()
















