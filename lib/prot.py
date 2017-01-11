# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 17:31:33
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-04 17:07:19
import time
import json
import hashlib
from pre_define import GlobalVar
DEBUG = True


def gen_id(dev_id=None):
    return dev_id + str(time.time())

def check_recv(func):
    def _deco(self, *recv):
        print self, recv, func.__name__ if bool(DEBUG) else 0
        try:

        except IndexError:
            raise Exception('lack of params')
    return _deco


def check_args(func):
    def _deco(self, *args):
        print self, args, func.__name__ if bool(DEBUG) else 0
        try:




class WebsocketProtocolConstructor(object):
    """
    with WebsocketProtocolConstructor(uid, _type) as ins:
            do something

        when exit <with> statments, del the WebsocketProtocol instance.
    """

    version = '1.0.0'

    def __init__(self, _type, uid=None):

        self.instance = WebsocketProtocol(uid=uid, _type=_type)

    def __enter__(self):
        """
        return WebsocketProtocol instance
        :return: <object>
        """

        return self.instance

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:
            del self.instance
        else:
            '''todo error log'''
            print exc_type, ': ', exc_val, '\n\t', exc_tb if bool(DEBUG) else 0


class WebsocketProtocol(object):

    version = '1.0.0'

    def __init__(self, _type):

        self._type = _type.lower()

        if self._type != 'request' and self._type != 'response':
            raise Exception('Wrong protocol type, "request" or "response" expected. '
                            'Got {err_type}.'.format(err_type=self._type))
        if self._type == 'request':
            self.uid = gen_id()

    @check_type
    def __request_pack(self, args, argv=None):

        return json.dumps(
            {
            "id": self.uid,
            "method": args,
            "params": argv
            }
        )

    @check_type
    def __response_pack(self, args, argv=None):

        return json.dumps(
            {
                "id": self.uid,
                "result": argv['result'],
                "msg": argv['msg']
            }
        )

    @check_type
    def __request_unpack(self, recv):

        message = json.loads(recv)

        uid = message['id']
        method = message['method']
        params = message['params']
        res = (uid, method, params)
        return res


    @check_type
    def __response_unpack(self, recv):

        message = json.loads(recv)

        try:
            if self._type == 'response':
                uid = message['id']
                result = message['result']
                msg = message['msg']
                res = (uid, result, msg)
                return res
            elif self._type == 'request':
                uid = message['id']
                method = message['method']
                params = message['params']
                res = (uid, method, params)
                return res
            else:
                raise Exception('No such post type: {t}'.format(t=self._type))
        except KeyError:
            # todo: error log
            print 'KeyError'

    @staticmethod
    def _ver():
        return WebsocketProtocol.version


if __name__ == "__main__":
    with WebsocketProtocolConstructor(_type='response') as wpins:
        res1 = wpins.pack('4213124125123', {"result": True, "msg": 'success'})
    print res1