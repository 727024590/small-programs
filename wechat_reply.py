#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基于itchat的微信自动回复设置，非工作时间处理公务是真的烦，所以写个程序来背锅。

author: zhuzi  date: 2019/04/20    version: 1.0
"""

import itchat
import time


# 对群消息进行自动回复
@itchat.msg_register('Text', isGroupChat = True)
def group_reply(msg):

    timestr = time.strftime("%m-%d %H:%M:%S", time.localtime())
    print('%s %s：%s' % (timestr, msg.actualNickName, msg.text))
    # 是否有人@自己
    if msg.isAt:
        itchat.send('%s %s：\n“%s”' % (timestr, msg.actualNickName, msg.text), toUserName = 'filehelper')
        return u'[自动回复]\n　　您好，我是机器人Diana，主人五一不在线，您的消息已收到，我会及时转达。'

# 对文本、图片、语音、视频、分享、附件内容进行自动回复
@itchat.msg_register(['Text', 'Picture', 'Recording', 'Video', 'Sharing', 'Attachment'])
def content_reply(msg):

    # 所有文本消息都给文件传输助手转发一份
    if msg['Type'] == 'Text':
        timestr = time.strftime("%m-%d %H:%M:%S", time.localtime())
        # 将不是自己发送的消息转发给文件助手
        if not msg.fromUserName == myUserName:
            print('%s %s：“%s”' % (timestr, msg.user.RemarkName, msg.text))
            #print('%s %s：“%s”' % (timestr, msg['User']['RemarkName'], msg['Content']))
            itchat.send('%s %s：\n“%s”' % (timestr, msg.user.RemarkName, msg.text), toUserName = 'filehelper')
        else:
            print('%s %s：“%s”' % (timestr, '自己', msg.text))
            
    return u'[自动回复]\n　　您好，我是机器人Diana~，主人五一不在线哦，小的会如实转达您的留言~'


if __name__ == '__main__':

    # 登录，命令行显示二维码，设置块字符的宽度为2，退出程序后暂存登录状态
    itchat.auto_login(enableCmdQR = 2, hotReload = True)
    myUserName = itchat.get_friends()[0]['UserName']
    itchat.run()
