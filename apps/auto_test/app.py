# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-10-24 11:26:15
# @Last Modified by:   hylide
# @Last Modified time: 2016-10-24 11:26:36

import json
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web

from handler.SingleQueryHandler import SingleQueryHandler
from lib.dict_objectified import DictObject

def launch(host, port, route):
	with open('service.config') as file:
		svr = DictObject(json.loads(file.read()))
	for i in svr.route:
        for j in i.values():
        impstring = "from handler.{pyfile} import {handler}".format(pyfile=)
	app = tornado.web.Application(
		handlers=[

		],
		debug=True,
	)
	http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()
