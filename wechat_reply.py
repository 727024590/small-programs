#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基于itchat的微信自动回复设置，非工作时间处理公务是真的烦，所以写个程序来背锅。

Author: Six  Date: 2019/04/20    Version: 1.0
Author: Six  Date: 2019/05/03    Version: 1.1     Function: 增加了图灵机器人
Author: Six  Date: 2019/05/18    Version: 1.2     Function: 增加自动回复的白名单机制
Author: Six  Date: 2019/06/24    Version: 1.3     Function: 增加了通过文件助手控制白名单的功能
"""

import itchat
import time
import random
import requests
import json
import re

# 对群消息进行自动回复
@itchat.msg_register('Text', isGroupChat=True)
def group_reply(msg):

    timestr = time.strftime("%m-%d %H:%M:%S", time.localtime())
    print('%s %s：%s' % (timestr, msg.actualNickName, msg.text))

    # 白名单中的群聊不进行自动回复
    #if msg['FromUserName'] in room_white_list:
    #    return None
    if msg.actualNickName in white_list_in_room:
        return None

    # 是否有人@自己
    if msg.isAt:
        time.sleep(random.uniform(0, 3))
        itchat.send(
            '%s %s：\n“%s”' %
            (timestr,
             msg.actualNickName,
             msg.text),
            toUserName='filehelper')

        robot_ans = tuling_reply(msg.text)
        print('%s %s：%s' % (timestr, 'Diana', robot_ans))
        time.sleep(random.uniform(0, 3))
        return robot_ans

# 对文本、语音内容进行自动回复
@itchat.msg_register(['Text', 'Recording'])
def content_reply(msg):

    timestr = time.strftime("%m-%d %H:%M:%S", time.localtime())

    # 接收手机端对文件助手发送的消息进行个性化处理
    if msg.toUserName == 'filehelper' and msg['Type'] == 'Text':
        # 使用正则判断name=open或name=close的形式对白名单进行临时增删
        namectl = re.match(r'^(\w+)=(open|close)$', msg.text)
        if namectl:
            if namectl.group(2) == 'open':
                white_list.discard(namectl.group(1))
                white_list_in_room.discard(namectl.group(1))
            else:
                white_list.add(namectl.group(1))
                white_list_in_room.add(namectl.group(1))
        return None

    # 白名单内的人不进行自动回复
    if msg.user.RemarkName in white_list:
        print('%s %s：“%s”' % (timestr, msg.user.RemarkName, msg.text))
        return None

    # 文本消息转发给文件助手并调用图灵机器人进行回复
    if msg['Type'] == 'Text':
        if msg.fromUserName == myUserName:
            print('%s %s：“%s”' % (timestr, '自己', msg.text))
            return None
        else:
            print('%s %s：“%s”' % (timestr, msg.user.RemarkName, msg.text))
            time.sleep(random.uniform(0, 3))
            itchat.send(
                '%s %s：\n“%s”' %
                (timestr,
                 msg.user.RemarkName,
                 msg.text),
                toUserName='filehelper')

        prefix = '【周末休息不在线，机器人回复】\n'
        now = time.time()
        # 如果同一人的消息冷却时间短于10分钟，则不加机器人回复的前缀
        if msg.user.RemarkName in usertime_dict:
            if now - usertime_dict[msg.user.RemarkName] < 600:
                prefix = ''
            usertime_dict[msg.user.RemarkName] = now
        else:
            usertime_dict[msg.user.RemarkName] = now

        robot_ans = ''.join([prefix, tuling_reply(msg.text)])
        print('%s %s：“%s”' % (timestr, 'Diana', robot_ans))
        return robot_ans

    time.sleep(random.uniform(0, 3))
    return (
        u'[自动回复] %s\n　　您好，我是助手Diana~，主人周末不在线，消息周一统一回复哦(^_^)' % timestr)


def tuling_reply(text):

    apiurl = 'http://openapi.tuling123.com/openapi/api/v2'
    # 读取图灵api
    with open('./data/tuling_api.txt', 'r') as f:
        apikey = f.readline().strip()
    data = {
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': apikey,
            'userId': 'Diana'
        }
    }
    r = requests.post(apiurl, data=json.dumps(data)).json()
    try:
        return r['results'][0]['values']['text']
    except KeyError:
        return r['results'][1]['values']['text'] + \
            '\n' + r['results'][0]['values']['url']


if __name__ == '__main__':

    # 登录，命令行显示二维码，设置块字符的宽度为2，退出程序后暂存登录状态
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    myUserName = itchat.get_friends()[0]['UserName']
    # 加载白名单，名单中的好友不自动回复
    with open('./data/white_list.txt', 'r') as f:
        white_list = set(f.read().splitlines())
    # 存放消息发送者发送上一条消息的时间
    usertime_dict = dict()

    # 获取通讯录中群聊，不进行自动回复
    #room_list = itchat.get_chatrooms(update=True)
    #room_white_list = []
    #for room in room_list:
    #    room_white_list.append(room['UserName'])
    # 名单中的人在群里发出的@消息不进行自动回复
    with open('./data/white_list_in_room.txt', 'r') as f:
        white_list_in_room = set(f.read().splitlines())

    itchat.run()
