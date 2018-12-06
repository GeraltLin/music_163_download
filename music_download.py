#coding: utf-8
"""
@Time : 2018/12/6 21:50
@Author : lin
"""
import requests
from urllib import request
from scrapy.selector import Selector
import os
import socket
#设置超时时间为30s
socket.setdefaulttimeout(30)
class wangyiyun():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Referer': 'http://music.163.com/'}
        self.main_url='http://music.163.com/'
        self.session = requests.Session()
        self.session.headers=self.headers

    def get_songurls(self,playlist):
        '''进入所选歌单页面，得出歌单里每首歌各自的ID 形式就是“song?id=64006"'''
        url=self.main_url+'playlist?id=%d'% playlist
        re= self.session.get(url)   #直接用session进入网页，懒得构造了
        sel=Selector(text=re.text)   #用scrapy的Selector，懒得用BS4了
        songurls=sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        return songurls   #所有歌曲组成的list
        ##['/song?id=64006', '/song?id=63959', '/song?id=25642714', '/song?id=63914', '/song?id=4878122', '/song?id=63650']

    def get_songinfo(self,songurl):
        '''根据songid进入每首歌信息的网址，得到歌曲的信息
        '''
        url=self.main_url+songurl
        re=self.session.get(url)
        sel=Selector(text=re.text)
        song_id = url.split('=')[1]
        song_name = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
        singer= '&'.join(sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
        songname=singer+'-'+song_name
        return str(song_id),songname

    def get_real_url(self,url):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'http://music.163.com/'}
        rs = requests.get(url, headers=headers, timeout=10)
        return rs.url


    def download_song(self, songurl, dir_path):
        '''根据歌曲url，下载mp3文件'''
        song_id, songname = self.get_songinfo(songurl)  # 根据歌曲url得出ID、歌名
        songname = songname.replace('/', ' ')
        if songname not in self.music_list:
            # print(songname)


            song_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%song_id

            song_url = self.get_real_url(song_url)

            path = dir_path + os.sep + songname + '.mp3'  # 文件路径

            request.urlretrieve(song_url, path)



    def work(self, playlist):
        songurls = self.get_songurls(playlist)  # 输入歌单编号，得到歌单所有歌曲的url

        for songurl in songurls:
            try:
                self.download_song(songurl, self.dir_path)  # 下载歌曲
            except Exception as e:
                print(e)
if __name__ == '__main__':
    import urllib
    # path = r'F:\音乐\1.mp3'
    # song_url = 'http://m10.music.126.net/20181206231944/4a6c5b8a95d897187b2af6e0b5678412/ymusic/66c0/2aaa/bf1c/c982d33d4364888d4ad82f3809f81932.mp3'
    # request.urlretrieve(song_url, path)
    path = r'F:\音乐'

    music_list = os.listdir(path)
    music_list = list(map(lambda x: x.split('.mp3')[0], music_list))
    d = wangyiyun()
    d.dir_path = path
    d.music_list = music_list
    d.work(118810280)
    # print(rst)
