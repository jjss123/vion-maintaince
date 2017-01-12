# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 17:31:33
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-04 17:07:19

import unittest
import sys

sys.path.append('..')

from lib import vmts_jsonrpc_protocol
from lib.vmts_jsonrpc_protocol import WebsocketProtocolConstructor as wpc

class TestWpc(unittest.TestCase):

    def setUp(self):
        print 'setUp debug mode = false'
        vmts_jsonrpc_protocol.DEBUG = False

    def test_request_pack(self):

        with wpc(_type='request') as w:
            res = w.pack('#id-test', 'method-test', {'params1':'a', 'params2': 'b'})

        self.assertEquals(res, '{"id": "#id-test", "method": "method-test", "params": {"params1":"a", "params2": "b"}')
        self.assertTrue(type(res) == str)

    def test_request_unpack(self):

        with wpc(_type='request') as w:
            res = w.unpack('{"params": {"params1": "a", "params2": "b"}, "id": "#id-test", "method": "method-test"}')

        self.assertEquals(res, ('#id-test', 'method-test', {"params1":"a", "params2": "b"}))
        self.assertTrue(type(res) == tuple)
        self.assertTrue(len(res) == 3)
        self.assertTrue(type(res[2]) == dict)

    def test_response_pack(self):

        with wpc(_type='response') as w:
            res = w.pack('#id-test', 'success', 'function is callable')

        self.assertEquals(res, '{"id": "#id-test", "result": "success", "msg": "function is callable"}')
        self.assertTrue(type(res) == str)

    def test_response_unpack(self):

        with wpc(_type='response') as w:
            res = w.unpack('{"id": "#id-test", "result": "success", "msg": "function is callable"}')

        self.assertEquals(res, ('#id-test', 'success', 'function is callable'))
        self.assertTrue(type(res) == tuple)
        self.assertTrue(len(res) == 3)
        self.assertTrue(type(res[2]) == str)

if __name__ == '__main__':
    unittest.main()