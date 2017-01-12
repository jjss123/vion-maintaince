# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 17:31:33
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-04 17:07:19
import time
import json

from pre_define import GlobalVar
DEBUG = True


def gen_id(dev_id=None):
    #todo: dev_id get value from GlobalVar
    if not dev_id:
        return str(time.time())
    return dev_id + str(time.time())

def check_recv(func):
    def _deco(self, *recv):
        print self, recv, func.__name__ if bool(DEBUG) else 0

        def check_key(key_lst, src_dict):
            for i in key_lst:
                if i not in src_dict:
                    return False

            return True

        if len(recv) > 1:
            # todo: custom exception
            raise
        try:
            recv_json = json.loads(recv[0])
        except ValueError:
            raise Exception('Wrong Type of json')
        try:
            if self._type == 'request':
                if not check_key(
                    ['id', 'method', 'params'],
                    recv_json
                ):
                    raise Exception('Wrong keys of input json')
                return func(self, recv_json)

            elif self._type == 'response':
                if not check_key(
                    ['id', 'result', 'msg'],
                    recv_json
                ):
                    raise Exception('Wrong keys of input json')

                return func(self, recv_json)
            else:
                raise Exception('Wrong type of protocol')
        except IndexError:
            raise Exception('lack of params')
    return _deco


def check_args(func):
    def _deco(self, *args, **argv):
        print self, args, func.__name__ if bool(DEBUG) else 0
        try:
            if self._type == 'request':
                if len(args) == 1:
                    return func(self, args, argv)
            elif self._type == 'response':
                if len(args) == 3:
                    return func(self, args[0], args[1], args[2])
        except IndexError:
            raise Exception('lack of params')
    return _deco


class WebsocketProtocolConstructor(object):
    """
    with WebsocketProtocolConstructor(uid, _type) as ins:
            do something

        when exit <with> statments, del the WebsocketProtocol instance.
    """

    version = '1.0.0'

    def __init__(self, _type):

        self.instance = WebsocketProtocol(_type=_type)

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
            #todo error log
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
            self.pack = self.__request_pack
            self.unpack = self.__request_unpack
        elif self._type == 'response':
            self.uid = None
            self.pack = self.__response_pack
            self.unpack = self.__response_unpack

    @check_args
    def __request_pack(self, method, **params):

        if not params:
            params = {}

        return json.dumps(
            {
            "id": self.uid,
            "method": method,
            "params": params
            }
        )

    @check_args
    def __response_pack(self, id, result, msg=None):

        return json.dumps(
            {
                "id": id,
                "result": result,
                "msg": msg
            }
        )

    @check_recv
    def __request_unpack(self, recv):

        return recv['id'], recv['method'], recv['params']


    @check_recv
    def __response_unpack(self, recv):

        return recv['id'], recv['result'], recv['msg']



    @staticmethod
    def _ver():
        return WebsocketProtocol.version


