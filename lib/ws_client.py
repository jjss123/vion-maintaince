# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 11:03:21
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-04 17:18:27

import time
import threading
import hashlib
import json
import websocket
import ws_protocol

def hash():
    hash_obj = hashlib.md5()
    hash_obj.update(str(time.time()))
    return hash_obj.hexdigest()

def on_message(ws, message):

    reply = ws_protocol.WebsocketProtocol(message)
    #msg = ws_protocol.WebsocketProtocol(protocol_init)

    if reply.msg_type == 'CONFIRM':
        print reply.message
        return 0


def on_error(ws, error):
    print error

def on_close(ws):
    print '### closed ###'

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
        'ws://localhost:8200/send',
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
        )
    ws.on_open = on_open
    ws.run_forever()
