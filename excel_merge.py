#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能：组合目录下所有Excel文件并按行内容计数

author: zhuzi   data: 2019/04/16    version: 1.0
"""

import os
import xlrd
import xlsxwriter

if __name__ == '__main__':

    # 获取文件名存为list
    files = os.listdir('./data/patient')
    result_dict = dict()

    for filename in files:
        book = xlrd.open_workbook('./data/patient/' + filename)
        # 读取文件中的第一个工作簿
        sheet = book.sheets()[0]

        for rowid in range(1, sheet.nrows): # 忽略表头
            content = tuple(sheet.row_values(rowid))
            if content not in result_dict:
                result_dict[content] = 1
            else:
                result_dict[content] += 1

    # 创建一个新Excel表
    book = xlsxwriter.Workbook('./data/patient.xlsx')
    # 添加Sheet
    sheet1 = book.add_worksheet('Sheet1')
    # 录入表头
    sheet1.write(0, 0, 'current')
    sheet1.write(0, 1, 'parent')
    sheet1.write(0, 2, 'relation')
    sheet1.write(0, 3, 'number')
    # 行号
    i = 1
    for k, v in result_dict.items():
        sheet1.write(i, 0, k[0])
        sheet1.write(i, 1, k[1])
        sheet1.write(i, 2, k[2])
        sheet1.write(i, 3, v)
        i += 1
    book.close()
