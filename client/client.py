 #
 # client.py
 # socket/client
 #
 # Created by 孙瑞琦 on 2019/12/15.
 # Copyright © 2019 孙瑞琦. All rights reserved.
 #

import socket
import os
import sys
import sendfile

host = input('请输入要连接到服务器：')
port = 10000

# 创建套接字
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

# 连接服务器
try:
    s.connect((host,port))
    print('服务器连接成功！')
except socket.error as msg:
    print('服务器连接失败：', msg)
    sys.exit(1)

# 数据收发
filepath = input('请选择要上传的文件（请确保使用的是UTF-8编码）：')
if os.path.isfile(filepath):
    # 如果是一个文件就发送
    sendfile.sendfile(s, filepath)
elif os.path.isdir(filepath):
    print('这是一个目录！')
    sys.exit(1)
else:
    print('文件不存在请检查！')
    sys.exit(1)
# 断开连接
# 这其实就是一个废步骤
s.shutdown(1)
# 关闭套接字
s.close()