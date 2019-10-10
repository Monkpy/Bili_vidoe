# -*- coding: utf-8 -*-
import json
import re

import requests


class Bilib(object):

    def __init__(self):

        # 请求主页面头
        self.getHtmlHeaders = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.bilibili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }

        # 下载视频请求头--不知道为什么要加
        self.downloadVideoHeaders = {
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/av24546213',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }

    # 获取网站源码
    def get_html(self, url):
        response = requests.get(url=url, headers=self.getHtmlHeaders)
        if response.status_code == 200:
            return response.text
        else:
            return response.status_code

    # 正则获取视频链接
    def get_link(self, html):
        links = []
        content = re.findall('window\.__playinfo__=(.*?)</script>', html, re.S)  # 获取视频所在的字典
        content = json.loads(content[0])  # 转换成字典
        durl = content['data']['durl']  # 逐步解析
        for cont in durl:
            if 'url' in cont.keys():
                video_url = cont['url']
                links.append(video_url)
        return links

    # 解析视频
    def parse_video(self, links):

        for i, link in enumerate(links):
            response = requests.get(link, headers=self.downloadVideoHeaders, stream=True)
            with open('./Bili_video' + str(i) + '.flv', 'wb') as f:
                print('开始下载第%s节' % i)
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

    def run(self):
        url = 'https://www.bilibili.com/video/av24546213/?p=1'
        html = self.get_html(url)
        links = self.get_link(html)
        self.parse_video(links)


if __name__ == '__main__':
    bilib = Bilib()
    bilib.run()

