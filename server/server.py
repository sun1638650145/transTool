 #
 # server.py
 # server
 #
 # Created by 孙瑞琦 on 2019/12/15.
 # Copyright © 2019 孙瑞琦. All rights reserved.
 #

import socket
import os
import oneconnect

# 有多个IP的时候可以指定一个IP，服务默认挂载在10000端口上
host = ''
port = 10000
savepath = './download/'
if not os.path.exists(savepath):
    os.mkdir(savepath)

# 创建套接字，bind()函数绑定端口
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

# 一直处于监听状态
while True:
    oneconnect.OneConnect(s)
