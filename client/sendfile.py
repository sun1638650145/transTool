 #
 # sendfile.py
 # client
 #
 # Created by 孙瑞琦 on 2019/12/15.
 # Copyright © 2019 孙瑞琦. All rights reserved.
 #

import struct
import os
import sys

def senddata(socket, filepath, checkpoint=0):
    """发送文件"""

    # 按照二进制流的方式打开文件，并移动到断点
    fp = open(filepath, 'rb')
    fp.seek(checkpoint)

    # 进度显示
    filesize = os.stat(filepath).st_size
    if checkpoint == 0:
        percent = 0.0
    else:
        percent = checkpoint * 1.0 / filesize
    if filesize < 1024:
        onepercent = 1.0
    else:
        onepercent = 1024.0 / filesize

    while True:
        data = fp.read(1024)
        if not data:
            print('{0}文件发送成功！'.format(os.path.basename(filepath)))
            break
        socket.send(data)
        percent += onepercent
        # 输出进度
        sys.stdout.write('\r%.4f%%' %(percent * 100))
        sys.stdout.flush()

def sendfile(socket, filepath):
    """使用sendfile函数传输文件"""

    # 发送文件名和文件大小
    filehead = struct.pack('128si', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
    socket.send(filehead)

    t = socket.recv(128)
    if t == b'exist and full':
        print('文件已经存在不需要上传')
        sys.exit(0)
    elif t == b'exist':
        r = socket.recv(64)
        checkpoint = int.from_bytes(r, byteorder='big', signed=False)
        print('断点是',checkpoint)
        senddata(socket, filepath, checkpoint)
    elif t == b'not exist':
        senddata(socket, filepath)
