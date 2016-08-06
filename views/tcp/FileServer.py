# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-19 09:28:15
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-19 09:28:45
import os
import struct

from tornado.tcpserver import TCPServer

class LargeFileSendHandler():
    clients = set()

    def __init__(self, stream, address):
        LargeFileSendHandler.clients.add(self)

        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        print self._address
        self.read_message()

    def read_message(self):
        self.fn = self._stream.read_until('\n').result()
        print self.fn
        self.send_message(self.fn)


    def send_message(self, fp):
        fp = os.path.dirname(__file__) + '/' + fp.replace('\n', '')
        print os.stat(fp).st_size
        sct = struct.Struct('I')
        head = sct.pack(os.stat(fp).st_size)
        self._stream.write(head)

        with open(fp, 'rb') as file:
            fc = file.read()

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
    
