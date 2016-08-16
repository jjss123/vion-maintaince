# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-08-16 16:30:10
# @Last Modified by:   hylide
# @Last Modified time: 2016-08-16 16:30:45

import sys
sys.path.append('../../')

from tornado import websocket
from model import pdbc_redis


class WebSockBrowserMainHandler(websocket.WebSocketHandler):

    clients = set()

    def open(self):
        if self not in WebSockBrowserMainHandler.clients:
            WebSockBrowserMainHandler.clients.add(self)
        self.stream.set_nodelay(True)
        print self.stream

    def on_message(self, message):
        ''''''

        print message
        self.write_message('confirm: ok')

    def on_close(self):
        WebSockBrowserMainHandler.clients.remove(self)



