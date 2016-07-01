# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 10:08:06
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-01 10:47:59
import os
import sys
import json
import time
import tornado.httpserver
import tornado.web
import tornado.ioloop
from tornado import websocket
sys.path.append('..')
from lib import ws_protocol

def msg_handler(msg):
    msg.msg_type =

class SendHandler(websocket.WebSocketHandler):
    clients = set()
    sequence = dict()

    def open(self):
        SendHandler.clients.add(self)
        self.stream.set_nodelay(True)

    def on_message(self, message):
        try:
            self.msg = ws_protocol.WebsocketProtocol(message)
        except TypeError, x:
            print x
            self.write_message(json.dumps({'Error': x }))
        except KeyError, x:
            print x
            self.write_message(json.dumps({'Error': x }))
        except NameError:
            if type(json.loads(message)) == 'dict':
                if json.loads(message)['Request'] == 'connect':
                    self.msg = ws_protocol.WebsocketProtocol(ws_protocol.WebsocketProtocol.protocol_init)
                    self.write_message(self.msg._msg)
        print self.msg
        message = json.loads(message)
        print type(message), message
        if type(message) == dict:
            if message[u'request'] == u'connect':
                self.write_message(json.dumps({'response':'success'}))
            else:
                self.write_message(json.dumps({'response':'response... %s'%message}))

    def on_close(self):
        SendHandler.clients.remove(self)



if __name__ == '__main__':
    app = tornado.web.Application(
        handlers = [
            (r"/send", SendHandler)
        ],
        debug = False
    )
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(8200)
    tornado.ioloop.IOLoop.instance().start()


