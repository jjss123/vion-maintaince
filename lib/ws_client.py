# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 11:03:21
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:14:55

import time
import threading
import hashlib
import base64
import json
import websocket
import ws_protocol

import tcp_client

def hash():
    hash_obj = hashlib.md5()
    hash_obj.update(str(time.time()))
    return hash_obj.hexdigest()

class MainConn():

    @staticmethod
    def on_message(ws, message):

        reply = ws_protocol.WebsocketProtocol(message)

        #msg = ws_protocol.WebsocketProtocol(protocol_init)

        if reply.msg_type == 'CONFIRM':
            print reply.message
            return 0

        elif reply.msg_type == 'POST':
            print reply.message
            file_name = reply.message['file_name']
            host = reply.message['server_host']
            port = int(reply.message['port'])
            tcp_client.transmit(host, port, file_name)

            return 0

    @staticmethod
    def on_error(ws, error):
        print error

    @staticmethod
    def on_close(ws):
        print '### closed ###'

    @staticmethod
    def on_open(ws):

        msg = ws_protocol.WebsocketProtocol(
            {
                'msg_type': 'LOGIN',
                'seq': hash(),
                'callback': None,
                'message': None
            })

        print 'connect'
        ws.send(msg._msg)

        def keeplive():
            while True:
                msg.seq = hash()
                ws.send(msg._msg)
                time.sleep(5)

        msg.msg_type = 'KeepLive'
        thread_keeplive = threading.Thread(target=keeplive, args=())
        thread_keeplive.setDaemon(True)
        thread_keeplive.start()

if __name__ == '__main__':
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        'ws://localhost:8200/ws/main',
        on_message = MainConn.on_message,
        on_error = MainConn.on_error,
        on_close = MainConn.on_close
        )
    ws.on_open = MainConn.on_open
    ws.run_forever()
