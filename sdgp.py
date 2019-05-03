#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
调用讯飞接口对文本进行语义依存分析，分析结果存储为三元组

author: zhuzi   version: 1.0 date: 2019/04/07
"""

import xlrd
import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
import xlsxwriter

# 从Excel中获取对话信息
def get_text(filepath):

    # 读取Excel文件
    data = xlrd.open_workbook(filepath)
    # 读取文件中的第1个工作簿
    sheet = data.sheets()[0]
    # 获取行数
    numrows = sheet.nrows
    
    textlist = []
    for rowid in range(1, numrows): # 不读取表头
        textlist.append(sheet.row_values(rowid)[4]) # 只读取对话内容

    return textlist

# 调用讯飞接口进行分词与依存分析，返回结果为list
def cws_and_sdgp(x_appid, api_key, text):

    #接口地址
    url ="http://ltpapi.xfyun.cn/v1/"

    body = urllib.parse.urlencode({'text': text}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000) 
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req_cws = urllib.request.Request(url + 'cws', body, x_header)
    req_sdgp = urllib.request.Request(url + 'sdgp', body, x_header)
    try:
        cws = urllib.request.urlopen(req_cws).read()
        print(cws)
    except urllib.error.HTTPError as e:
        print('urllib.error.HTTPError: ', e)
        return None
    try:
        sdgp = urllib.request.urlopen(req_sdgp).read()
        print(sdgp)
    except urllib.error.HTTPError as e:
        print('urllib.error.HTTPError: ', e)
        return None

    return [cws, sdgp]

# 解析json数据并抽取三元组存放到list中
def tuple_extract(row):

    # 存放三元组
    final = []
    cwsdict = json.loads(row[0])
    sdgpdict = json.loads(row[1])
    try:
        for arc in sdgpdict['data']['sdgp']:
            # 创建三元组，依次存储当前节点、父节点、关系
            record = [cwsdict['data']['word'][arc['id']], cwsdict['data']['word'][arc['parent']], arc['relate']]
            final.append(record)
    except KeyError as k:
        print('KeyError: ', k)

    return final

# 从Excel中获取API的key
def get_apikey(filepath):

    # 读取Excel文件
    data = xlrd.open_workbook(filepath)
    # 读取文件中的第1个工作簿
    sheet = data.sheets()[0]
    # 获取行数
    numrows = sheet.nrows
    
    apikey_list= []
    for rowid in range(1, numrows): # 不读取表头
        apikey_list.append(sheet.row_values(rowid))

    return apikey_list

if __name__ == '__main__':

    # 获取对话文本
    textlist = get_text('./data/data_clean_v1.13_doctor.xlsx')
    # 获取API的key
    apikey_list = get_apikey('./data/apikey.xlsx')

    # 存放每次抽取出的三元组
    final = []
    # 数据的起始处理位置
    start = 0
    # MD，给SB师姐写程序，这也就罢了，竟然还打算让我手动干这么多活，幸亏大哥机智，小改一下程序批量处理
    for eachid in apikey_list:
        x_appid = eachid[0]
        api_key = eachid[1]
        # 每次处理500条数据
        for i in range(start, start + 500):
            text = textlist[i]
            row = cws_and_sdgp(x_appid, api_key, text)
            if row == None:
                time.sleep(60)
                continue
            time.sleep(0.06)
            final += tuple_extract(row)

        # 创建一个Excel表
        book = xlsxwriter.Workbook('./data/doctor_' + str(start + 500) +'.xlsx')
        # 添加Sheet1
        sheet1 = book.add_worksheet('Sheet1')
        # 录入表头
        sheet1.write(0, 0, 'current')
        sheet1.write(0, 1, 'parent')
        sheet1.write(0, 2, 'relation')

        i = 1   # 行号
        for row in final:
            sheet1.write(i, 0, row[0])
            sheet1.write(i, 1, row[1])
            sheet1.write(i, 2, row[2])
            i += 1

        book.close()
        start += 500 
        final = []
