#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
从维基百科某词条开始，一直跳转并存储第一个链接，直到抵达“哲学”词条或陷入循环或达到最大次数。

Author: Six     Date: 2019/11/28    Version: 1.0
"""

import time
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup

def firstlink_get(url):
    """给定链接，返回该链接下的首链接

    url: 给定的链接
    """

    # 添加代理，socks5h：用代理服务器解析主机域名
    proxies = {
        'http': 'socks5h://127.0.0.1:1080',
        'https': 'socks5h://127.0.0.1:1080'
    }
    response = requests.get(url, proxies=proxies)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    firstlink = None
    # 根据维基百科页面结构获取首链接
    contents = soup.find(id='mw-content-text').find(class_='mw-parser-output').contents
    # 下面用的方法有点笨了，find方法有recursive参数可直接调节只在子节点范围内寻找
    for content in contents:
        # 找到正文第一段
        if content.name == 'p':
            for item in content.contents:
                # 找到首链接
                if item.name == 'a':
                    firstlink = 'https://zh.wikipedia.org' + item.get('href')
                    break
            break

    return firstlink


def spider_body(url='https://zh.wikipedia.org/wiki/%E7%BB%B4%E5%9F%BA%E7%99%BE%E7%A7%91', max_iters=25, interval=2):
    """程序主体，返回链接list.

    url: 第一次链接人为给出，默认“维基百科”
    max_iters: 最大链接次数，默认25
    interval: 采集频率，默认2s
    """

    # 记录词条跳转路径
    url_list = list()

    # 达到最大跳转次数则退出循环
    while len(url_list) < max_iters:
        # 直接从链接获取url表示的词条
        word = unquote(url).strip('/').split('/')[-1]
        # 没有页面或陷入循环或无链接则退出迭代
        if word.startswith('index.php?') or {word: url} in url_list or url is None:
            break

        url_list.append({word: url})
        print(word)
        # 词条为“哲学”则退出迭代
        if word == '哲学':
            break

        # 获取链接下的首链接
        url = firstlink_get(url)
        time.sleep(interval)

    return url_list


if __name__ == '__main__':

    print(spider_body('https://zh.wikipedia.org/wiki/%E6%9B%BC%E5%93%88%E9%A1%BF%E8%AE%A1%E5%88%92'))
