 #
 # sendfile.py
 # socket/client
 #
 # Created by 孙瑞琦 on 2019/12/15.
 # Copyright © 2019 孙瑞琦. All rights reserved.
 #

import struct
import os

def sendfile(socket, filepath):
    """使用sendfile函数传输文件"""

    # 发送文件名和文件大小
    filehead = struct.pack('128si', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
    socket.send(filehead)

    # 按照二进制流的方式打开文件
    fp = open(filepath, 'rb')
    while True:
        data = fp.read(1024)
        if not data:
            print('{0}文件发送成功！'.format(os.path.basename(filepath)))
            break
        socket.send(data)
