# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-19 10:19:39
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-19 10:37:51

import socket
import struct
import time

HOST = '127.0.0.1'
PORT = 8202
BUFSIZE = 1024
FILEINFO_SIZE = struct.calcsize('I')

def transmit(host, port, file_name, save_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((host, port))
            break
        except:
            print 'retrying ...'
            time.sleep(1)
            continue
    print 'connected.'

    s.sendall('%s\n'%file_name)    
    head = s.recv(FILEINFO_SIZE)
    file_size = struct.unpack('I', head)[0]
    print file_size
    restsize = file_size

    with open("../files/{save_name}".format(save_name=save_name), 'wb') as file:
        while True:
            if restsize > BUFSIZE:
                data = s.recv(BUFSIZE)
            else:
                data = s.recv(restsize)

            file.write(data)

            restsize = restsize - len(data)
            if restsize == 0:
                break

    s.close()

if __name__ == '__main__':
    transmit('127.0.0.1', 8201,'test')
