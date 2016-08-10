# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-19 10:19:39
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-19 10:37:51

import socket
import struct
import time

def transmit(host, port, buff,file_name, save_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    while True:
        try:
            s.connect((host, port))
            break
        except:
            print 'retrying ...'
            time.sleep(1)
            continue
    print 'connected.'

    s.sendall('{fn}\n'.format(fn=file_name))

    try:
        head = s.recv(struct.calcsize('I'))
        file_size = struct.unpack('I', head)[0]
        print file_size
        restsize = file_size

        with open("../files/{save_name}".format(save_name=save_name), 'wb') as file:
            while True:
                if restsize > buff:
                    data = s.recv(buff)
                else:
                    data = s.recv(restsize)

                file.write(data)

                restsize = restsize - len(data)
                if restsize == 0:
                    break
    except socket.error, e:
        print e.message
        s.close()
        transmit(host, port, buff,file_name, save_name)

    s.close()
    return True

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8202
    BUFSIZE = 1024
    transmit('127.0.0.1', 8201,'test')
