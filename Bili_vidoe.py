# -*- coding:utf-8 -*-
import json
import re

import requests


class Bili(object):

    def __init__(self):
        self.GetHtmlResponse = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.bilibili.com',
            'Referer': 'https://search.bilibili.com/all?keyword=%E6%9F%AF%E5%9F%BA%E5%90%B5%E6%9E%B6&from_source=nav_search_new',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }
        self.DownloadVideoHeaders = {
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/av41727997?from=search&seid=10011971736294746765',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }

    def get_html(self, url):
        response = requests.get(url, headers=self.GetHtmlResponse)
        if response.status_code == 200:
            # print(response.text)
            return response.text
        else:
            print('Get Html Code is False:%s' % response.status_code)

    def get_link(self, html):
        links = []
        content = re.findall('window\.__playinfo__=(.*?)</script>', html, re.S)  # 获取视频所在的字典
        # print(content)
        content = json.loads(content[0])  # 转换成字典
        # print(content)
        durl = content['data']['dash']['video']  # 逐步解析
        for cont in durl:
            if 'baseUrl' in cont.keys():
                video_url = cont['baseUrl']
                links.append(video_url)
        return links

    def parse_vidoe(self, links):
        for i, link in enumerate(links):
            response = requests.get(link, headers=self.DownloadVideoHeaders, stream=True)
            with open('./Vidoe/' + str(i) + '.flv', 'wb') as f:
                print('开始下载第%s节' % i)
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

    def main(self):
        url = 'https://www.bilibili.com/video/av41727997?from=search&seid=10011971736294746765'
        html = self.get_html(url)
        links = self.get_link(html)
        self.parse_vidoe(links)


if __name__ == '__main__':
    bili = Bili()
    bili.main()

