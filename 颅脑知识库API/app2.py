#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from owlready2 import *

"""
关于颅脑数据的一个接口，接口参数详见Web API.txt

author: zhuzi   date: 2019/04/12    version: 1.0
"""


app = Flask(__name__)
CORS(app)
with open('./pickle2.dat', 'rb') as f:
    tumors_info = pickle.load(f)
    classes = pickle.load(f)
    tree_data = pickle.load(f)


# 使用GET请求获取所有数据
@app.route('/data/all', methods=['GET'])
def data_all():
    return json.dumps(tumors_info)


# 通过POST请求提供检索API，头字段"content-type:application/json"，根据检索内容返回json
# 可检索字段为"tumorNameEn", "NameInCN", "MeshCode", "ICD_10Code", "ICD_OCode"
@app.route('/data/retrieval', methods=['post'])
def retrieval():
    retrieval_data = request.get_json()
    retrieval_attr = retrieval_data['attr']
    retrieval_value = retrieval_data['value']
    # 设定支持检索的字段的集合
    attr_set = (
        'tumorNameEn',
        'NameInCN',
        'MeshCode',
        'ICD_10Code',
        'ICD_OCode')

    # 存放检索结果
    result = {
        'code': '',     # '0': 'success', '1': 'no match', '2': 'AttrError'
        'desc': '',
        'data': []
    }
    if retrieval_attr in attr_set:
        for record_key in tumors_info:
            # 字符串化的原因是'content'下的内容既有str又有list，不方便统一处理
            if retrieval_value in str(tumors_info[record_key]['content'][retrieval_attr]):
                result['code'] = '0'
                result['desc'] = 'success'
                result['data'].append(tumors_info[record_key])
    else:
        result['code'] = '2'
        result['desc'] = 'AttrError'

    if not result['code']:
        result['code'] = '1'
        result['desc'] = 'no match'

    return json.dumps(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5200)
