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
import hashlib

def computefilemd5(filepath):
    """计算文件的md5值"""

    hash = hashlib.md5()
    fp = open(filepath, 'rb')
    while True:
        b = fp.read(4096)
        if not b:
            break
        hash.update(b)
    fp.close()

    return hash.hexdigest()

def sendfilemd5(socket, filepath):
    """发送文件的md5值"""

    # 计算md5值
    sendmd5 = computefilemd5(filepath)

    # 发送给服务器
    md5head = struct.pack('32si', sendmd5.encode('utf-8'), 0)
    socket.send(md5head)

    # 接收服务器的校验结果
    ans = socket.recv(128)
    if ans == b'True':
        return True
    else:
        return False

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
        sys.stdout.write('\rINFO:%.3f%%' %(percent * 100))
        sys.stdout.flush()

    fp.close()

    # 发送md5并核验
    if sendfilemd5(socket, filepath) is True:
        print("INFO:经md5核验文件准确无误")
        sys.exit(0)
    else:
        print("INFO:经md5核验文件有误，建议重新发送")
        sys.exit(1)

def sendfile(socket, filepath):
    """使用sendfile函数传输文件"""

    # 发送文件名和文件大小
    filehead = struct.pack('128si', os.path.basename(filepath).encode('utf-8'), os.stat(filepath).st_size)
    socket.send(filehead)

    t = socket.recv(128)
    if t == b'exist and full':
        print('INFO:文件已经存在不需要上传，', end='')

        # 发送md5并核验
        if sendfilemd5(socket, filepath) is True:
            print("经md5核验文件准确无误")
            sys.exit(0)
        else:
            print("经md5核验文件有误，建议检查是否由同名文件")
            sys.exit(1)

    elif t == b'exist':
        r = socket.recv(64)
        checkpoint = int.from_bytes(r, byteorder='big', signed=False)
        print('INFO:断点是', checkpoint)
        senddata(socket, filepath, checkpoint)
    elif t == b'not exist':
        senddata(socket, filepath)