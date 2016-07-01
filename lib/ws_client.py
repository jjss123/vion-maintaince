# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 11:03:21
# @Last Modified by:   riposa
# @Last Modified time: 2016-06-16 15:56:18

import websocket
import thread
import time
import json


def on_message(ws, message):
    message = json.loads(message)
    if message['response'] == 'success':
        print message
        ws.send(json.dumps('hello world'))
    else:
        print message
    #ws.closed()

def on_error(ws, error):
    print error

def on_close(ws):
    print '### closed ###'

def on_open(ws):
    '''def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send(json.dumps('hello world'))

    thread.start_new_thread(run, ())'''
    print 'send'
    ws.send(json.dumps({'request':'connect'}))

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
