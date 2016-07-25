# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-25 11:09:19
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-25 11:26:46

import os
import multiprocessing
import inspect

import tornado.httpserver
import tornado.web
import tornado.ioloop

from config import Config, Route

tcp_start = ws_start = False

for i in Route.web_views:
    viewstring = "from views.web import {view}".format(view=i)
    exec viewstring

if Config.FileServer.start_when == "host_start":
    import tcp_server
    tcp_start = True

if Config.WebSocketServer.start_when == "host_start":
    import websocket_server
    ws_start = True


def run():
    app = tornado.web.Application(
        handlers=[(i, eval(Route.web_route.__getattribute__(i))) for i in Route.web_route.keys()],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(Config.Website.port)
    tornado.ioloop.IOLoop.instance().start()

def start_server():
    proc = list()

    web = multiprocessing.Process(target=run)
    web.start()
    proc.append(web)
    print 'http server started ...'
    if tcp_start:
        tcp = multiprocessing.Process(target=tcp_server.run)
        tcp.start()
        proc.append(tcp)
        print 'tcp server started ...'
    if ws_start:
        ws = multiprocessing.Process(target=websocket_server.run)
        ws.start()
        proc.append(ws)
        print 'websocket server started ...'

    for i in proc:
        i.join()
if __name__ == "__main__":
    start_server()


