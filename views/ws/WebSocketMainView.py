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
import json

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
        self.msg.check_method('Client')

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
            id = self.msg.message['dev_id']
            query = pdbc_redis.DeviceInterface.objects.filter(dev_id=id)
            if query.all().__len__() == 1:
                query.first().status = '1'
                query.first().service_status = json.dumps(self.msg.message['service'])
            else:
                raise ValueError('cannot find this device.')
            query.first().is_valid()
            query.first().save()

            self.reply.message = {'KeepAlive': 'success'}
            self.write_message(self.reply._msg)

        def status_handler():
            id = self.msg.message['dev_id']
            if self.msg.message.has_key('static'):
                query = pdbc_redis.DeviceInterface.objects.filter(dev_id=id)
                if query.all().__len__() == 1:
                    query.first().ip = self.msg.message['source']
                    query.first().type = self.msg.message['dev_type']
                    query.first().name = self.msg.message['name']
                    query.first().status = '1'
                    query.first().static_info = json.dumps(self.msg.message['static'])

                    query.first().is_valid()
                    query.first().save()
                elif query.all().__len__() == 0:
                    query = pdbc_redis.DeviceInterface(
                        dev_id=id,
                        ip = self.msg.message['source'],
                        type = self.msg.message['dev_type'],
                        name = self.msg.message['name'],
                        status = '1',
                        static_info = json.dumps(self.msg.message['static'])
                    )

                    query.is_valid()
                    query.save()

            elif self.msg.message.has_key('dynamic'):
                query = pdbc_redis.DeviceDynamicInterface(
                    dev_id = id,
                    timestamp = datetime.datetime.fromtimestamp(
                        self.msg.message['timestamp']
                    ),
                    dynamic_info = self.msg.message['dynamic']
                )
                query.is_valid()
                query.save()

            self.reply.message = {'Status': 'success'}
            self.write_message(self.reply._msg)

        if self.msg.method == 'Login':
            WebSockMainHandler.login[self] = True
            self.source = self.msg.message['source']
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
                eval(self.msg.method.lower() + '_handler')()
                return 0

    @classmethod
    def broad_cast(cls, file_name, callback_type='shell',callback=None, *dev):
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
            if '{' in callback:
                callback = callback.replace('{iplast}', str(i.source.split('.')[-1]))
            i.reply.callback = callback
            if i.proxy_host:
                s_host = i.proxy_host
            else:
                s_host = Config.host
            i.reply.message = {
                'file_name': '../../files/' + file_name,
                'save_name': file_name,
                'server_host': s_host,
                'port': 18202,
                'callback_type': callback_type.lower()
            }
            i.write_message(i.reply._msg)


class TriggerHandler(tornado.web.RequestHandler):
    def get(self):
        callback = self.get_argument("callback")
        callback_type = self.get_argument("callback_type")
        WebSockMainHandler.broad_cast(self.get_argument("file"), callback_type=callback_type,callback=callback)



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



