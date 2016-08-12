# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-19 09:28:15
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-19 09:28:45
import os
import struct
import time

from tornado.tcpserver import TCPServer

class LargeFileSendHandler():
    clients = set()

    def __init__(self, stream, address):
        LargeFileSendHandler.clients.add(self)

        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        print self._address, LargeFileSendHandler.clients.__len__()
        self.read_message()

    def read_message(self):
        count = 0
        while True:
            if count > 10:
                raise Exception('zombie threadhold, need to reconnect')
            try:
                self.fn = self._stream.read_until('\n').result()
                break
            except:
                time.sleep(1)
                count += 1
                continue
        print self.fn

        self.send_message(self.fn.strip())


    def send_message(self, fp):
        fp = os.path.dirname(__file__) + '/' + fp
        print os.stat(fp).st_size
        sct = struct.Struct('I')
        head = sct.pack(os.stat(fp).st_size)
        self._stream.write(head)

        with open(fp, 'rb') as file:
            fc = file.read()

        print self._address, 'start sending'
        self._stream.write(fc)


    def on_close(self):
        LargeFileSendHandler.clients.remove(self)

        print 'one client quit', self._address
        print 'only {clients} clients remain'.format(clients=str(LargeFileSendHandler.clients.__len__()))

class FileSendServer(TCPServer):

    def handle_stream(self, stream, address):
        LargeFileSendHandler(stream, address)


if __name__ == '__main__':
    from tornado.ioloop import IOLoop
    server = FileSendServer()
    server.listen(8201)
    print 'server start ...'
    IOLoop.instance().start()
    
