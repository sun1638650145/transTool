 #
 # receivefile.py
 # server
 #
 # Created by 孙瑞琦 on 2019/12/15.
 # Copyright © 2019 孙瑞琦. All rights reserved.
 #

import os
import struct

def computesize(fn, byte):
    """计算大小"""

    if byte * 1.0 / 1e9 > 1:
        Gb = byte * 1.0 / 1e9
        print('传输的文件名是{0}，文件大小是{1}GB'.format(str(fn), Gb))
    elif byte * 1.0 / 1e6 > 1:
        Mb = byte * 1.0 / 1e6
        print('传输的文件名是{0}，文件大小是{1}MB'.format(str(fn), Mb))
    elif byte * 1.0 / 1e3 > 1:
        Kb = byte * 1.0 / 1e3
        print('传输的文件名是{0}，文件大小是{1}KB'.format(str(fn), Kb))
    else:
        print('传输的文件名是{0}，文件大小是{1}Bytes'.format(str(fn), byte))

def computecheckpoint(filepath):
    """计算断点"""

    int_checkpoint_size = os.stat(filepath).st_size
    # 将int转换成byte
    byte_checkpoint_size = int_checkpoint_size.to_bytes(length=64, byteorder='big', signed=False)
    return int_checkpoint_size, byte_checkpoint_size

def recvdata(socket, savepath, filename, filesize, checkpoint=0):
    """接收文件"""

    # 从头接收文件或者断点开始接收
    if checkpoint == 0:
        fp = open(str(savepath) + str(filename), 'wb')
    else:
        fp = open(str(savepath) + str(filename), 'ab')

    # 按照二进制流的方式接收文件
    print('开始接收...')
    recvd_size = checkpoint
    while not recvd_size == filesize:
        if filesize - recvd_size > 1024:
            data = socket.recv(1024)
            recvd_size += 1024
        # 不可整除部分
        else:
            data = socket.recv(filesize - recvd_size)
            recvd_size = filesize

        # 写入文件
        fp.write(data)

    fp.close()
    print('文件接收成功！')

def recvfile(socket, savepath):
    """使用recvfile函数接收文件"""

    # 定义基本信息的格式
    file_info = struct.calcsize('128si')
    buf = socket.recv(file_info)

    if buf:
        # 获取文件名和文件大小
        filename, filesize = struct.unpack('128si', buf)
        fn = filename.strip(b'\00')
        fn = fn.decode(encoding='UTF-8')
        computesize(fn, filesize)

        if os.path.exists(str(savepath) + str(fn)) and os.stat(str(savepath) + str(fn)).st_size == filesize:
            s = '文件已经存在'
            s_b = b'exist and full'
            socket.send(s_b)
            print(s)
        elif os.path.exists(str(savepath) + str(fn)) and os.stat(str(savepath) + str(fn)).st_size != filesize:
            s = '文件已经存在部分，将进行断点续传'
            s_b = b'exist'
            socket.send(s_b)

            # 计算断点
            checkpoint, num = computecheckpoint(str(savepath) + str(fn))
            socket.send(num)
            print(s)
            recvdata(socket, savepath, fn, filesize, checkpoint)
        else:
            print('本地不存在该文件，', end='')
            s_b = b'not exist'
            socket.send(s_b)
            recvdata(socket, savepath, fn, filesize)
