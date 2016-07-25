# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-25 14:27:00
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-25 14:54:02
import tornado.httpserver
import tornado.web
import tornado.ioloop

from config import Config, Route

for i in Route.ws_views:
    viewstring = "from views.ws import {view}".format(view=i)
    exec viewstring

def run():
    app = tornado.web.Application(
        handlers=[(i, eval(Route.ws_route.__getattribute__(i))) for i in Route.ws_route.keys()],
        debug=True
    )

    websocket_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    websocket_server.listen(Config.WebSocketServer.port)
    tornado.ioloop.IOLoop.instance().start()