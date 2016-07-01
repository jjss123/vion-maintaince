# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 17:31:33
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-01 10:36:57
import json
import hashlib
import time

class WebsocketProtocol(object):

    version = '1.0.0'
    author = 'hylide'
    protocol_init = json.dumps(
    {
        'msg_type':'LOGIN',
        'seq':'1',
        'callback': None,
        'message':'connected'
    }
    )

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
        if type(message) == str:
            message = json.loads(message)
        elif type(message) == dict:
            pass
        else:
            raise TypeError('Receive Wrong Type Message')
        self.msg_type = message['msg_type']
        if message['seq']:
            self.seq = message['seq']
        else:
            hash_obj = hashlib.md5()
            hash_obj.update(str(time.time()))
            hash_code = hash_obj.hexdigest()
            self.seq = hash_code
        self.callback = message['callback']
        self.message = message['message']

    def __getattributelist__(self):
        return ['msg_type', 'seq', 'callback', 'message']

    def _ver(self):
        return WebsocketProtocol.version

if __name__ == '__main__':
    hash_obj_t = hashlib.md5()
    hash_obj_t.update(str(time.time))
    hash_code_t = hash_obj_t.hexdigest()
    test = WebsocketProtocol(json.dumps(
        {
            'msg_type':'LOGIN',
            'seq':hash_code_t,
            'callback':{
                'function':'nullable'
            },
            'message':{
                'cpu':'123124',
                'mem':'4421421'
            }
        })
        )
    print test
    print test._msg
    print test.msg_type
    print test.seq
    print test.message
    try:
        print isinstance(test, WebsocketProtocol)
    except NameError, x:
        print x

    test1 = WebsocketProtocol(
        {
            'msg_type':'LOGIN',
            'seq':hash_code_t,
            'callback':{
                'function':'nullable'
            },
            'message':{
                'cpu':'123124',
                'mem':'4421421'
            }
        }
        )
    print test1
    print test1._msg
    print test1.msg_type
    print test1.seq
    print test1.message



