 #
 # server.py
 # server
 #
 # Created by 孙瑞琦 on 2019/12/15.
 # Copyright © 2019 孙瑞琦. All rights reserved.
 #

import socket
import sys
import receivefile as rc
import os

# 有多个IP的时候可以指定一个IP，服务默认挂载在10000端口上
host = ''
port = 10000
savepath = 'download/'
if not os.path.exists(savepath):
    os.mkdir(savepath)


# 创建套接字，bind()函数绑定端口
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

# 监听请求
s.listen(1)
print('服务器已正常运行')

# 接收请求，并建立连接
try:
    conn, addr = s.accept()
    print('成功建立连接，客户端地址是：', addr)
except socket.error as msg:
    print('连接失败：', msg)
    sys.exit(1)

# 收发数据
rc.recvfile(conn, 'download/')
# 断开连接
conn.shutdown(1)
# 关闭套接字
conn.close()