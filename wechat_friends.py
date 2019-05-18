#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""""
使用itchat获取微信好友列表并进行分析。

author: zhuzi   version: 1.0    date: 2019/05/18    function: 将好友信息录入Excel
"""

import itchat
import pickle
import xlsxwriter

if __name__ == '__main__':

    itchat.auto_login(True)

    friend_list = itchat.get_friends(update = True)
    with open('./data/wechat_friends_pickle.dat', 'wb') as fw:
        pickle.dump(friend_list, fw)

    with open('./data/wechat_friends_pickle.dat', 'rb') as fr:
        friend_list = pickle.load(fr)
    with xlsxwriter.Workbook('./data/wechat_friends.xlsx') as book:
        sheet1 = book.add_worksheet('Sheet1')
        attr_list = [
            'Uin',
            'UserName',
            'NickName',
            'HeadImgUrl',
            'ContactFlag',
            'MemberCount',
            'RemarkName',
            'HideInputBarFlag',
            'Sex',
            'Signature',
            'VerifyFlag',
            'OwnerUin',
            'AppAccountFlag',
            'Statues',
            'AttrStatus',
            'Province',
            'City',
            'Alias',
            'SnsFlag',
            'UniFriend',
            'DisplayName',
            'ChatRoomId',
            'KeyWord',
            'EncryChatRoomId',
            'IsOwner']
        # 按行写入，前两个参数分别为行和列的索引
        sheet1.write_row(0, 0, attr_list)
        for row_index in range(len(friend_list)):
            content = []
            for attr in attr_list:
                try:
                    content.append(friend_list[row_index][attr])
                except KeyError:
                    content.append('None')
            sheet1.write_row(row_index + 1, 0, content)
