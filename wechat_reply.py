#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基于itchat的微信自动回复设置，非工作时间处理公务是真的烦，所以写个程序来背锅。

author: Six  date: 2019/04/20    version: 1.0
author: Six  date: 2019/05/03    version: 1.1     function: 增加了图灵机器人
author: Six  date: 2019/05/18    version: 1.2     function: 增加自动回复的白名单机制
"""

import itchat
import time
import random
import requests
import json

# 对群消息进行自动回复
@itchat.msg_register('Text', isGroupChat=True)
def group_reply(msg):

    timestr = time.strftime("%m-%d %H:%M:%S", time.localtime())
    print('%s %s：%s' % (timestr, msg.actualNickName, msg.text))

    if msg['FromUserName'] in room_white_list:
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
        time.sleep(random.uniform(0, 3))
        return (
            u'[自动回复] %s\n　　您好，我是助手Diana，主人端午放假不在线，您的消息已收到，我会及时转达。\n【消息以"$"开头我可以陪您聊天哦】' %
            timestr)
    # 以'$'开头的文本调用图灵机器人进行回复
    if msg.text.startswith('$') or msg.text.startswith('＄'):
        robot_ans = tuling_reply(msg.text.lstrip('$＄'))
        time.sleep(random.uniform(0, 3))
        return robot_ans

# 对文本、图片、语音、视频、分享、附件内容进行自动回复
@itchat.msg_register(['Text', 'Picture', 'Recording',
                      'Video', 'Sharing', 'Attachment'])
def content_reply(msg):

    timestr = time.strftime("%m-%d %H:%M:%S", time.localtime())
    if (msg['FromUserName'] in white_list) or (
            msg.user.RemarkName in white_list):
        print('%s %s：“%s”' % (timestr, msg.user.RemarkName, msg.text))
        return None

    # 所有文本消息都给文件传输助手转发一份
    if msg['Type'] == 'Text':
        # 以'$'开头的文本调用图灵机器人进行回复
        if msg.text.startswith('$') or msg.text.startswith('＄'):
            print('%s %s：“%s”' % (timestr, msg.user.RemarkName, msg.text))
            #print('%s %s：“%s”' % (timestr, msg['User']['RemarkName'], msg['Content']))
            robot_ans = tuling_reply(msg.text.lstrip('$＄'))
            time.sleep(random.uniform(0, 3))
            return robot_ans
        # 将不是自己发送的消息转发给文件助手
        if not msg.fromUserName == myUserName:
            print('%s %s：“%s”' % (timestr, msg.user.RemarkName, msg.text))
            time.sleep(random.uniform(0, 3))
            itchat.send(
                '%s %s：\n“%s”' %
                (timestr,
                 msg.user.RemarkName,
                 msg.text),
                toUserName='filehelper')
        else:
            print('%s %s：“%s”' % (timestr, '自己', msg.text))

    time.sleep(random.uniform(0, 3))
    return (
        u'[自动回复] %s\n　　您好，我是助手Diana~，主人端午放假不在线，消息周一统一回复(^_^)\n【试试以"$"开头进行回复可以和我聊天哦[奸笑]】' %
        timestr)


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
        white_list = f.read().splitlines()

    # 获取通讯录中群聊，不进行自动回复
    room_list = itchat.get_chatrooms(update=True)
    room_white_list = []
    for room in room_list:
        room_white_list.append(room['UserName'])

    itchat.run()
