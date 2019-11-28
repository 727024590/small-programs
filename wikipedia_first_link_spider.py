#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
从维基百科某词条开始，一直跳转并存储第一个链接，直到抵达“哲学”词条或陷入循环或达到最大次数。

Author: Six     Date: 2019/11/28    Version: 1.0
"""

import time

def word_link_get(url):
    """给定链接，返回该链接代表的词条与链接下的首链接

    url: 给定的链接
    """

    return word, firstlink


def spider_body(url='https://zh.wikipedia.org/wiki/%E5%93%B2%E5%AD%A6', max_iters=25, interval=2):
    """程序主体，返回链接list.

    url: 第一次链接人为给出，默认“维基百科”
    max_iters: 最大链接次数，默认25
    interval: 采集频率，默认2s
    """

    # 记录词条跳转路径
    url_list = list()

    # 达到最大跳转次数则退出循环
    while len(url_list) < max_iters:
        # 获取链接表示的词条和该链接下的首链接
        word, firstlink = word_link_get(url)
        url_list.append({url: word})

        # 词条为“哲学”或陷入循环则退出迭代
        if word == '哲学' or firstlink in url_list:
            break

        url = firstlink
        time.sleep(interval)

    return url_list
