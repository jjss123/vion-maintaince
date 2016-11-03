# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-25 11:09:19
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-25 11:26:46
import os
import sys

import tornado.httpserver
import tornado.web
import tornado.ioloop

from config import config, route

for i in route.web_views:
    viewstring = "from views.web import {view}".format(view=i)
    exec viewstring

def run():
    settings = config.Website.settings
    app = tornado.web.Application(
        handlers=[(i, eval(route.web_route.__getattribute__(i))) for i in route.web_route.keys()],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(config.Website.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    args = sys.argv
    run()