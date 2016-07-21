# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 10:08:06
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:23:57
import os
import sys
import hashlib
import base64
import json
import time
import tornado.httpserver
import tornado.web
import tornado.ioloop
from tornado import websocket
sys.path.append('..')
from lib import ws_protocol

def hash():
    hash_obj = hashlib.md5()
    hash_obj.update(str(time.time()))
    return hash_obj.hexdigest()

class WebSockMainHandler(websocket.WebSocketHandler):
    clients = set()
    login = dict()

    def open(self):
        if self not in WebSockMainHandler.clients:
            WebSockMainHandler.clients.add(self)
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
        WebSockMainHandler.clients.remove(self)

    def error_reply(self, msg):
        self.reply.message = {'Error': msg}
        self.write_message(self.reply._msg)
        self.on_close()

    def msg_handler(self):

        if self.msg.msg_type == 'LOGIN':
            WebSockMainHandler.login[self] = True
            self.reply.msg_type = 'CONFIRM'
            self.reply.message = {'login': 'success'}
            self.write_message(self.reply._msg)
            return 0

        if self not in WebSockMainHandler.login.keys():
            self.error_reply('need login, connection refused')
            return 0
        else:
            if not WebSockMainHandler.login[self]:
                self.error_reply('logged out, connection refused')
                return 0
            else:
                self.reply.seq = self.msg.seq
                self.reply.msg_type = 'CONFIRM'

        if self.msg.msg_type == 'LOGOUT':
            WebSockMainHandler.login[self] = False
            self.reply.message = {'logout': 'success'}
            self.write_message(self.reply._msg)
            self.on_close()
        elif self.msg.msg_type == 'KeepLive':
            self.reply.message = {'keeplive': 'success'}
            self.write_message(self.reply._msg)
        else:
            pass
        return 0

    @classmethod
    def broad_cast(cls, file_name, *dev):
        seq = hash()
        if dev:
            cli = dev
        else:
            cli = WebSockMainHandler.clients

        for i in cli:
            i.reply = ws_protocol.WebsocketProtocol(ws_protocol.WebsocketProtocol.protocol_post)
            i.reply.seq = seq
            i.reply.message = {
                'file_name': file_name,
                'server_host': '127.0.0.1',
                'port': '8201'
            }
            i.write_message(i.reply._msg)


class TriggerHandler(tornado.web.RequestHandler):
    def get(self):
        WebSockMainHandler.broad_cast('test')
        #return 'send broadcast!'

class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("dashboard.html",User='Cirno', comment='baka')

class TestSuitHandler(tornado.web.RequestHandler):
    def get(self):
        suit = self.get_argument('suit')
        if suit == 'maintaince':
            self.render("testsuit-maintaince.html",User='Cirno', comment='baka')

if __name__ == '__main__':
    app = tornado.web.Application(
        handlers = [
            (r"/ws/main", WebSockMainHandler),
            (r"/ws/broadcast", TriggerHandler),
            (r"/", MainPageHandler),
            (r"/testsuit", TestSuitHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "..\\templates"),
        static_path=os.path.join(os.path.dirname(__file__), "..\\static"),
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(8200)
    tornado.ioloop.IOLoop.instance().start()



