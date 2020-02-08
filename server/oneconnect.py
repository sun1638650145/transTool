 #
 # oneconnect.py
 # server
 #
 # Created by 孙瑞琦 on 2019/12/16.
 # Copyright © 2019 孙瑞琦. All rights reserved.
 #

import socket
import receivefile as rc
import sys
import os

def OneConnect(s):
    # 监听请求
    s.listen(1)
    print('INFO:服务器已正常运行')

    # 接收请求，并建立连接
    try:
        conn, addr = s.accept()
        print('INFO:成功建立连接，客户端地址是：', addr)
    except socket.error as msg:
        print('ERROR:连接失败：', msg)
        sys.exit(1)

    # 收发数据
    if not os.path.exists('./download'):
        os.makedirs('./download/')
    rc.recvfile(conn, './download/')
    # 断开连接
    conn.shutdown(1)
    # 关闭套接字
    conn.close()
    print('INFO:当前进程已正常结束')