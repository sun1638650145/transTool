 #
 # client.py
 # client
 #
 # Created by 孙瑞琦 on 2019/12/15.
 # Copyright © 2019 孙瑞琦. All rights reserved.
 #

import socket
import os
import sys
import sendfile

host = input('INFO:请输入要连接到服务器：')
port = 10000

# 创建套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
try:
    s.connect((host,port))
    print('INFO:服务器连接成功！')
except socket.error as msg:
    print('ERROR:服务器连接失败：', msg)
    sys.exit(1)

# 数据收发
filepath = input('INFO:请选择要上传的文件（请确保使用的是UTF-8编码）：')
if os.path.isfile(filepath):
    # 如果是一个文件就发送
    sendfile.sendfile(s, filepath)
elif os.path.isdir(filepath):
    print('ERROR:这是一个目录！')
    sys.exit(1)
else:
    print('ERROR:文件不存在请检查！')
    sys.exit(1)
# 断开连接
s.shutdown(1)
# 关闭套接字
s.close()
