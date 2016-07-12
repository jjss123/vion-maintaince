# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 10:08:06
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:23:57
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



class SendHandler(websocket.WebSocketHandler):
    clients = set()
    login = dict()

    def open(self):
        if self not in SendHandler.clients:
            SendHandler.clients.add(self)
        else:
            print 'warning: unclosed connection %s'%str(self)
        self.stream.set_nodelay(True)

    def on_message(self, message):
        ''''''

        # message protocol check
        self.reply = ws_protocol.WebsocketProtocol(ws_protocol.WebsocketProtocol.protocol_init)
        print message, type(message)
        try:
            self.msg = ws_protocol.WebsocketProtocol(message)
        except TypeError, x:
            print x
            self.error_reply(str(x))
            return 0

        # main handler of event 'on_message'
        self.msg_handler()

    def on_close(self):
        SendHandler.clients.remove(self)

    def error_reply(self, msg):
        self.reply.message = {'Error': msg}
        self.write_message(self.reply._msg)
        self.on_close()

    def msg_handler(self):

        if self.msg.msg_type == 'LOGIN':
            SendHandler.login[self] = True
            self.reply.msg_type = 'CONFIRM'
            self.reply.message = {'login': 'success'}
            self.write_message(self.reply._msg)
            return 0

        if self not in SendHandler.login.keys():
            self.error_reply('need login, connection refused')
            return 0
        else:
            if not SendHandler.login[self]:
                self.error_reply('logged out, connection refused')
                return 0
            else:
                self.reply.seq = self.msg.seq
                self.reply.msg_type = 'CONFIRM'

        if self.msg.msg_type == 'LOGOUT':
            SendHandler.login[self] = False
            self.reply.message = {'logout': 'success'}
            self.write_message(self.reply._msg)
            self.on_close()
        elif self.msg.msg_type == 'KeepLive':
            self.reply.message = {'keeplive': 'success'}
            self.write_message(self.reply._msg)
        else:
            pass
        return 0

class TriggerHandler(tornado.web.RequestHandler):
    def get(self):
        all_send()
        #return 'send broadcast!'

def all_send():
    for i in SendHandler.clients:
        i.reply = ws_protocol.WebsocketProtocol(ws_protocol.WebsocketProtocol.protocol_init)
        i.reply.message = 'this is a broadcast post from server'
        i.write_message(i.reply._msg)


if __name__ == '__main__':
    app = tornado.web.Application(
        handlers = [
            (r"/send", SendHandler),
            (r"/broadcast", TriggerHandler)
        ],
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(8200)
    tornado.ioloop.IOLoop.instance().start()


