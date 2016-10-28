# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-08-16 16:30:10
# @Last Modified by:   hylide
# @Last Modified time: 2016-08-16 16:30:45

import time
import hashlib
import json

from tornado import websocket
from model import pdbc_redis
from lib.dict_objectified import DictObject

def hash(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

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
        self.msg = DictObject(json.loads(message))
        print message
        self.msg_handler()

    def msg_handler(self):
        ''''''

        method = self.msg.method
        message = self.msg.message
        timestamp = self.msg.timestamp

        # handle start here
        def get_device_status_handler():

            # todo: need format
            cli_hash = hash(str(message['localStorage']))
            # todo: need exception
            try:
                svr_hash = pdbc_redis.DeviceInterfaceHash.objects.filter(hash_anchor='vmts').first().hash_str
            except AttributeError:
                # todo: need calculate hash string
                print 'need requery'
                res = pdbc_redis.DeviceInterface.objects.all()
                content = list()
                for i in res:
                    dev_info = dict()
                    dev_info['id'] = i.dev_id
                    dev_info['status'] = "Online" if i.status else "Offline"
                    dev_info['ip'] = i.ip
                    dev_info['name'] = i.name
                    dev_info['type'] = i.type
                    dev_info['static'] = i.static_info
                    content.append(dev_info)
                hash_dev_str = hash(str(content))
                new_hash = pdbc_redis.DeviceInterfaceHash(
                    hash_anchor='vmts',
                    hash_str=hash_dev_str
                )
                if new_hash.is_valid() and new_hash.save():
                    svr_hash = hash_dev_str
                else:
                    raise Exception('can not hash.')

            if cli_hash == svr_hash:
                # device list has keeped up-to-date, no need to refreshing
                reply = {
                    "method": "Confirm",
                    "timestamp": time.time(),
                    "message": {
                        "from_request": message["request"],
                        "result": "No action",
                        "commet": "Is up-to-date, no need of refreshing."
                    }
                }
                self.reply = json.dumps(reply)
                self.write_message(self.reply)
                return 0
            else:
                # device list has changed, must refresh the data
                reply = {
                    "method": "Confrim",
                    "timestamp": time.time(),
                    "message": {
                        "from_request": message["request"],
                        "result": "Prepare to Refresh",
                        "commet": "Is not up-to-date, must refresh the data."
                    }
                }
                self.reply = json.dumps(reply)
                self.write_message(self.reply)

                # refresh data start here

                res = pdbc_redis.DeviceInterface.objects.all()
                content = list()
                for i in res:
                    dev_info = dict()
                    dev_info['id'] = i.dev_id
                    dev_info['status'] = "Online" if i.status else "Offline"
                    dev_info['ip'] = i.ip
                    dev_info['name'] = i.name
                    dev_info['type'] = i.type
                    dev_info['static'] = i.static_info
                    content.append(dev_info)

                reply = {
                    "method": "Refresh",
                    "timestamp": time.time(),
                    "message": {
                        "type": "static",
                        "content":content
                    }
                }

                self.reply = json.dumps(reply)
                print self.reply
                self.write_message(self.reply)

        if method.lower() == "login".lower():
            WebSockBrowserMainHandler.login[self] = True
            # todo: optional single instance
            reply = {
                "method": "Confirm",
                "timestamp": time.time(),
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
                "timestamp": time.time(),
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
                    "timestamp": time.time(),
                    "message": {
                        "from_request": method,
                        "success": False,
                        "reason": "Log, connection refused"
                    }
                }
                self.reply = json.dumps(reply)
                self.write_message(self.reply)
            else:
                eval(method.lower() + '_' + message['request'].lower() + '_handler')()
                return 0

    def on_close(self):
        WebSockBrowserMainHandler.clients.remove(self)
        WebSockBrowserMainHandler.login[self] = False



