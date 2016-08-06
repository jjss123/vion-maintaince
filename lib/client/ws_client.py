# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 11:03:21
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:14:55

import hashlib
import os
import sys
import threading
import time

import psutil
import websocket
import ConfigParser

import tcp_client
import info_collection.static
import info_collection.dynamic
import ws_protocol

default_conf = {
    'base': {
        'url': 'ws://192.168.5.222:8201/ws/main',
        'net_interface': 'eth0'
    },
    'task-0': {
        'name': 'keep-alive',
        'enable': True,
        'interval': 5
    },
    'task-1': {
        'name': 'dynamic-status',
        'enable': True,
        'interval': 60
    },
    'proxy': {
        'enable': True,
        'host': '192.168.5.222'
    }
}

def hash():
    hash_obj = hashlib.md5()
    hash_obj.update(str(time.time()))
    return hash_obj.hexdigest()

class MainConn():

    @staticmethod
    def on_message(ws, message):

        reply = ws_protocol.WebsocketProtocol(message)

        print reply.message
        if reply.method == 'Confirm':

            return 0

        elif reply.method == 'Transmit':
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

        elif reply.method == 'Set':

            # todo
            return 0



    @staticmethod
    def on_error(ws, error):
        print error

    @staticmethod
    def on_close(ws):
        print '### closed ###'

    @staticmethod
    def on_open(ws):

        # login message
        msg_login = ws_protocol.WebsocketProtocol(
            {
                'method': 'Login',
                'seq': hash(),
                'callback': None,
                'message': {
                    "proxy": load_config('proxy')['enable'],
                    "proxy_host": load_config('proxy')['host'],
                    "source": LOCAL_IP
                }
            })

        print 'connect'
        ws.send(msg_login._msg)

        # static message
        msg_static_status = ws_protocol.WebsocketProtocol(
            {
                'method': 'Status',
                'seq': None,
                'callback': None,
                'message': {
                    'timestamp': None,
                    'source': LOCAL_IP,
                    'static': info_collection.static.get()
                }
            }
        )
        ws.send(msg_static_status._msg)

        # task keep-alive
        keep_alive_conf = load_config(keys=['task'])['keep-alive']
        if keep_alive_conf['enable']:
            msg_keep_alive = ws_protocol.WebsocketProtocol(
                {
                    'method': 'KeepAlive',
                    'seq': None,
                    'callback': None,
                    'message':{
                        'timestamp': None,
                        'source': LOCAL_IP,
                        'service': info_collection.dynamic.service_status()
                    }
                }
            )

            def keep_alive(interval):
                while True:
                    msg_keep_alive.seq = hash()
                    msg_keep_alive.message["timestamp"] = time.time()
                    ws.send(msg_keep_alive._msg)
                    time.sleep(interval)

            thread_keepAlive = threading.Thread(target=keep_alive, args=(keep_alive_conf['interval'], ))
            thread_keepAlive.setDaemon(True)
            thread_keepAlive.start()

        # task dynamic status
        dynamic_status_conf = load_config(keys=['task'])['dynamic-status']
        if dynamic_status_conf['enabel']:
            msg_dynamic_status = ws_protocol.WebsocketProtocol(
                {
                    'method': 'Status',
                    'seq': None,
                    'callback': None,
                    'message':{
                        'timestamp': None,
                        'source': LOCAL_IP,
                        'dynamic': info_collection.dynamic.get()
                    }
                }
            )

            def dynamic_status(interval):
                while True:
                    msg_dynamic_status.seq = hash()
                    msg_dynamic_status.message["timestamp"] = time.time()
                    ws.send(msg_dynamic_status._msg)
                    time.sleep(interval)

            thread_dynamicStatus = threading.Thread(target=dynamic_status, args=(dynamic_status_conf['interval'], ))
            thread_dynamicStatus.setDaemon(True)
            thread_dynamicStatus.start()



def load_config(fp='./ws_client.conf', *keys):
    conf = ConfigParser.ConfigParser()
    if FP:
        fp = FP
    # conf initialize
    if not os.path.isfile(fp):
        for i in default_conf.keys():
            conf.add_section(i)
            for j in default_conf[i].keys():
                conf.set(i, j, default_conf[i][j])
        conf.write(fp)

    # conf read
    conf.read(fp)

    def get_value(section, option):
        try:
            if type(option) == list:
                res = dict()
                for i in option:
                    res[i] = (conf.get(section, i))
                return res
            return conf.get(section=section, option=option)
        except ConfigParser.NoOptionError:
            return 'default'
        except ConfigParser.NoSectionError:
            return 'default'

    cf = {
        'url': get_value('base', 'url'),
        'proxy': get_value('proxy', 'host'),
        'net_interface': get_value('base', 'net_interface')
    }

    if keys:
        if 'task' in keys:
            tasklist = dict()
            for k in conf.sections():
                if 'task' in k:
                    tasklist[get_value(k, 'name')] = get_value(k, conf.options(k))
            cf['task'] = tasklist
        res = dict()
        for i in keys:
            res[i] = cf[i]
        return res
    else:
        tasklist = dict()
        for k in conf.sections():
            if 'task' in k:
                tasklist[get_value(k, 'name')] = get_value(k, conf.options(k))
        cf['task'] = tasklist
        return cf

def set_config(section, option, value, fp='./ws_client.conf'):
    if FP:
        fp = FP

    conf = ConfigParser.ConfigParser()
    conf.read(fp)
    conf.set(section=section, option=option, value=value)
    conf.write(fp)

if __name__ == '__main__':
    #websocket.enableTrace(True)
    conf_fp = sys.argv[1]
    if conf_fp:
        FP = conf_fp
    else:
        FP = ''

    ws_url = load_config()['url']
    ws_proxy = load_config()['proxy']

    local_ip = list()
    for i in psutil.net_if_addrs()['eth0']:
        if i.family == 2:
            local_ip.append(i.address)

    LOCAL_IP = local_ip

    ws = websocket.WebSocketApp(
        ws_url,
        on_message = MainConn.on_message,
        on_error = MainConn.on_error,
        on_close = MainConn.on_close
        )
    ws.on_open = MainConn.on_open
    ws.run_forever()
