#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计高频词对的关系，按行排列，即每行一对词。

author: zhuzi   data: 2019/04/17    version: 1.0
"""

import xlrd
import xlsxwriter

if __name__ == '__main__':

    book = xlrd.open_workbook('./data/共现词对.xlsx')
    result_book = xlsxwriter.Workbook('./data/sdgp_statistic.xlsx')
    # 工作簿内有两个表
    for sheet_id in range(2):
        result_dict = dict()
        sheet = book.sheets()[sheet_id]
        for rowid in range(1, sheet.nrows): # 忽略表头
            content = sheet.row_values(rowid)
            cp = content[0] + '-' + content[1]    # current + parent
            pc = content[1] + '-' + content[0]    # parent + current
            relation = content[2]
            number = content[3]
            if cp in result_dict:
                if relation in result_dict[cp]:
                    result_dict[cp][relation] += number
                else:
                    result_dict[cp][relation] = number
            elif pc in result_dict:
                if relation in result_dict[pc]:
                    result_dict[pc][relation] += number
                else:
                    result_dict[pc][relation] = number
            else:
                result_dict[cp] = dict()
                # 将关系及其数量录入子字典
                result_dict[cp][relation] = number

        # 写入结果
        result_sheet = result_book.add_worksheet('Sheet' + str(sheet_id))
        result_sheet.write(0, 0, 'pair words')
        result_sheet.write(0, 1, 'relation_types')
        result_sheet.write(0, 2, 'relation')
        result_sheet.write(0, 3, 'number')
        # 行号
        i = 1
        for k, v in result_dict.items():
            result_sheet.write(i, 0, k)
            result_sheet.write(i, 1, len(result_dict[k]))
            # 列号
            j = 2
            for relation, number in result_dict[k].items():
                result_sheet.write(i, j, relation)
                result_sheet.write(i, j + 1, result_dict[k][relation])
                j += 2
            i += 1
    result_book.close()
