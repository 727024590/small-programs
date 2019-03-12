#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模拟两台电脑的进程间通信，进程A将系列字符串发送到进程B，由进程B负责将其转换为utf-8编码形式并将结果传回进程A；
IPC_master.py负责启动发送进程，IPC_worker.py负责启动处理进程。

参考代码：https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431929340191970154d52b9d484b88a7b343708fcc60000

author: zhuzi   version: 1.0    date: 2019/03/12
"""

import queue
from multiprocessing.managers import BaseManager

# 发送任务的队列
task_queue = queue.Queue()
# 接收结果的队列
result_queue = queue.Queue()

class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上，callable参数关联了Queue对象
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000,设置验证码'zhuzi'
manager = QueueManager(address=('', 5000), authkey=b'zhuzi')
# 启动Queue
manager.start()
# 获得通过网络访问的Queue对象
task = manager.get_task_queue()
result = manager.get_result_queue()

# 这里只进行一次编码任务
content = input('Please input your strings to endode with UTF-8:')
task.put(content)
# 获取结果
print('The result is %s' % result.get())

manager.shutdown()
print('Master is over!')
