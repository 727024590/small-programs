#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
将master进程传来的字符(串)编码为utf-8并返回

参考代码：https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431929340191970154d52b9d484b88a7b343708fcc60000

author: zhuzi   version: 1.0    date: 2019/03/12
"""

import queue
from multiprocessing.managers import BaseManager

# 创建类似的QueueManager
class QueueManager(BaseManager):
    pass

# 由于只从网络上获取Queue，所以注册时只提供名字
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到运行IPC_master.py的服务器
m = QueueManager(address=('127.0.0.1', 5000), authkey=b'zhuzi')
m.connect()

# 获取Queue的对象
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列获取任务并将结果录入result队列
n = task.get()
print('receive: %s' % n)
r = n.encode('utf-8')
print('transform to UTF-8: %s' % r)
result.put(r)

print('Worker is over!')
