# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-08-16 16:30:10
# @Last Modified by:   hylide
# @Last Modified time: 2016-08-16 16:30:45

import datetime
import hashlib
import json
import sys
sys.path.append('../../')

from tornado import websocket
from model import pdbc_redis

def hash(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

class WebSocketBrowserProtocol(object):

    def __init__(self, dict_obj):
        keys = dict_obj.keys()
        for i in keys:
            if type(dict_obj[i]) == dict:
                self.__setattr__(i, WebSocketBrowserProtocol(dict_obj[i]))
            else:
                self.__setattr__(i, dict_obj[i])

    def __repr__(self):
        return self.__dictionary__()

    def __str__(self):
        return str(self.__repr__())

    def __getitem__(self, item):
        if isinstance(self.__getattribute__(item), WebSocketBrowserProtocol):
            return self.__getattribute__(item).__str__()
        else:
            return self.__getattribute__(item)

    def __dictionary__(self):
        attr = self.__dict__
        for i in attr.keys():
            if isinstance(attr[i], WebSocketBrowserProtocol):
                attr[i] = attr[i].__dictionary__()
        return attr

    def keys(self):
        return self.__dict__.keys()

    def has_key(self, key):
        if key in self.__dict__.keys():
            return True
        else:
            return False

class WebSockBrowserMainHandler(websocket.WebSocketHandler):

    clients = set()
    login = dict()

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in WebSockBrowserMainHandler.clients:
            WebSockBrowserMainHandler.clients.add(self)
        self.stream.set_nodelay(True)
        print self.stream

    def on_message(self, message):
        ''''''
        self.msg = WebSocketBrowserProtocol(json.loads(message))
        print message
        self.msg_handler()

    def msg_handler(self):
        ''''''

        method = self.msg.method
        message = self.msg.message
        timestamp = self.msg.timestamp

        if method.lower() == "login".lower():
            WebSockBrowserMainHandler.login[self] = True
            # todo: optional single instance
            reply = {
                "method": "Confirm",
                "timestamp": datetime.datetime.ctime(),
                "message": {
                    "from_request": "Login",
                    "success": True
                }
            }
            self.reply = json.dumps(reply)
            self.write_message(self.reply)
            return 0

        if self not in WebSockBrowserMainHandler.login.keys():
            reply = {
                "method": "Confirm",
                "timestamp": datetime.datetime.ctime(),
                "message": {
                    "from_request": method,
                    "success": False,
                    "reason": "Need login, connection refused"
                }
            }
            self.reply = json.dumps(reply)
            self.write_message(self.reply)
            return 0
        else:
            if not WebSockBrowserMainHandler.login[self]:
                reply = {
                    "method": "Confirm",
                    "timestamp": datetime.datetime.ctime(),
                    "message": {
                        "from_request": method,
                        "success": False,
                        "reason": "Log, connection refused"
                    }
                }

    def on_close(self):
        WebSockBrowserMainHandler.clients.remove(self)
        WebSockBrowserMainHandler.login[self] = False



