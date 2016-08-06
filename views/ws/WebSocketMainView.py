# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 10:08:06
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:23:57
import os
import sys
import hashlib
import time
import datetime

import tornado.web
from tornado import websocket
sys.path.append('../../')
from lib import ws_protocol
from config import Config
from model import pdbc_redis

__all__ = ["WebSockMainHandler", "TriggerHandler"]

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
            self.proxy_host = None
        else:
            print 'warning: unclosed connection %s'%str(self)
        self.stream.set_nodelay(True)

    def on_message(self, message):
        ''''''

        # message protocol check
        self.reply = ws_protocol.WebsocketProtocol(
            {
                'method': None,
                'seq': None,
                'callback': None,
                'message': None
            }
        )

        # format recv message
        self.msg = ws_protocol.WebsocketProtocol(message)
        self.msg.check_method('Server')

        # main handler of event 'on_message'
        self.msg_handler()

    def on_close(self):
        WebSockMainHandler.clients.remove(self)

    def error_reply(self, msg):
        self.reply.message = {'Error': msg}
        self.write_message(self.reply._msg)
        self.on_close()

    def msg_handler(self):

        def logout_handler():
            WebSockMainHandler.login[self] = False
            self.reply.message = {'logout': 'success'}
            self.write_message(self.reply._msg)
            self.on_close()
            
        def keepalive_handler():
            query = pdbc_redis.DeviceInterface(
                dev_ip=self.msg.message['source'],
                timestamp=datetime.datetime.fromtimestamp(
                    self.msg.message['timestamp']
                ),
                status=self.msg.message['1']
            )
            query.is_valid()
            query.save()

            self.reply.message = {'keeplive': 'success'}
            self.write_message(self.reply._msg)

        if self.msg.method == 'Login':
            WebSockMainHandler.login[self] = True
            if self.msg.message['proxy']:
                self.proxy_host = self.msg.message['proxy_host']
            self.reply.method = 'Confirm'
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
                eval(self.msg.method.lower() + 'handler')()
                return 0

    @classmethod
    def broad_cast(cls, file_name, callback=None, *dev):
        seq = hash()
        if dev:
            cli = dev
        else:
            cli = WebSockMainHandler.clients

        for i in cli:
            i.reply = ws_protocol.WebsocketProtocol(
                {
                    'method': 'Transmit',
                    'seq': None,
                    'callback': None,
                    'message': None
                }
            )
            i.reply.seq = seq
            i.reply.callback = callback
            if i.proxy_host:
                s_host = i.proxy_host
            else:
                s_host = Config.host
            i.reply.message = {
                'file_name': '../../files/' + file_name,
                'save_name': file_name,
                'server_host': s_host,
                'port': Config.FileServer.port
            }
            i.write_message(i.reply._msg)


class TriggerHandler(tornado.web.RequestHandler):
    def get(self):
        callback = self.get_argument("callback")
        WebSockMainHandler.broad_cast(self.get_argument("file"), callback=callback)



if __name__ == '__main__':
    import tornado.httpserver
    import tornado.web
    import tornado.ioloop
    app = tornado.web.Application(
        handlers = [
            (r"/ws/main", WebSockMainHandler),
            (r"/ws/broadcast", TriggerHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "..\\templates"),
        static_path=os.path.join(os.path.dirname(__file__), "..\\static"),
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(8200)
    tornado.ioloop.IOLoop.instance().start()



