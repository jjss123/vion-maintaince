# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 17:31:33
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-04 17:07:19
import json
import hashlib
import time

class MethodError(Exception):
    def __init__(self, content):
        Exception.__init__()
        self.message = content

class WebsocketProtocol(object):

    version = '1.0.0'
    author = 'hylide'
    allowed_method = {
        'Server':[
            'Transmit',
            'Get',
            'Set',
            'Confirm'
        ],
        'Client':[
            'Transmit',
            'Confirm',
            'KeepAlive',
            'Status'
        ]
    }
    
    @property
    def _msg(self):
        p = dict()
        for i in self.__getattributelist__():
            p[i] = self.__getattribute__(i)
        return json.dumps(p)

    @_msg.setter
    def _msg(self, value):
        if type(json.loads(value)) != dict:
            raise TypeError('Wrong message, must be dict')
        else:
            value = json.loads(value)
            for i in self.__getattributelist__():
                if i not in value.keys():
                    raise KeyError('Wrong protocol, must have key-%s'%i)
                else:
                    self.__setattr__(i, value[i])

    def __init__(self, message):
        if type(message) == str or type(message) == unicode:
            message = json.loads(message)
        elif type(message) == dict:
            pass
        else:
            raise TypeError('Receive Wrong Type Message')
        self.method = message['method']
        if message['seq']:
            self.seq = message['seq']
        else:
            hash_obj = hashlib.md5()
            hash_obj.update(str(time.time()))
            hash_code = hash_obj.hexdigest()
            self.seq = hash_code
        self.callback = message['callback']
        self.message = message['message']

    def check_method(self, side):
        if self.method not in WebsocketProtocol.allowed_method[side.capitalize()]:
            raise MethodError('Uncorrect method')


    def __getattributelist__(self):
        return ['method', 'seq', 'callback', 'message']

    def _ver(self):
        return WebsocketProtocol.version
