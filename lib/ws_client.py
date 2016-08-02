# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 11:03:21
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:14:55

import time
import os
import sys
import threading
import hashlib
import websocket
import psutil

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
            save_name = reply.message['save_name']
            host = reply.message['server_host']
            port = int(reply.message['port'])
            tcp_client.transmit(host, port, file_name, save_name)

            if reply.callback:
                print 'exec callback ...'
                os.system("echo {content} > temp.sh".format(content=reply.callback))
                os.system("chmod 775 temp.sh")
                os.system("./temp.sh")
            return 0



    @staticmethod
    def on_error(ws, error):
        print error

    @staticmethod
    def on_close(ws):
        print '### closed ###'

    @staticmethod
    def on_open(ws):

        msg_login = ws_protocol.WebsocketProtocol(
            {
                'msg_type': 'LOGIN',
                'seq': hash(),
                'callback': None,
                'message': {
                    "proxy": ws_proxy,
                    "proxy_host": ws_proxy_host
                }
            })

        print 'connect'
        ws.send(msg_login._msg)

        msg_keep_live = ws_protocol.WebsocketProtocol(
            {
                'msg_type': 'keeplive',
                'seq': None,
                'callback': None,
                'message':{
                    'timestamp': None,
                    'source': LOCAL_IP
                }
            }
        )

        msg_status = ws_protocol.WebsocketProtocol(
            {
                'msg_type': 'STATUS',
                'seq': None,
                'callback': None,
                'message':{
                    'timestamp': None,
                    'source': LOCAL_IP,
                    'status': None
                }
            }
        )

        def keeplive():
            while True:
                msg_keep_live.seq = hash()
                msg_keep_live.message["timestamp"] = time.time()
                ws.send(msg_keep_live._msg)
                time.sleep(5)

        def status():
            while True:
                msg_status.message["timestamp"] = time.time()
                msg_status.message["status"] =

        msg_keep_live.msg_type = 'KeepLive'
        thread_keeplive = threading.Thread(target=keeplive, args=())
        thread_keeplive.setDaemon(True)
        thread_keeplive.start()

if __name__ == '__main__':
    #websocket.enableTrace(True)
    ws_url = sys.argv[1]
    ws_proxy = bool(int(sys.argv[2]))

    local_ip = list()
    for i in psutil.net_if_addrs()['eth0']:
        if i.family == 2:
            local_ip.append(i.address)

    LOCAL_IP = local_ip

    if ws_proxy:
        ws_proxy_host = sys.argv[3]
    ws = websocket.WebSocketApp(
        ws_url,
        on_message = MainConn.on_message,
        on_error = MainConn.on_error,
        on_close = MainConn.on_close
        )
    ws.on_open = MainConn.on_open
    ws.run_forever()
