# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-25 14:27:12
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-25 14:54:12
import tornado.ioloop

from config import config
from views.tcp.FileServer import FileSendServer

def run():
    server = FileSendServer()
    server.listen(config.FileServer.port)
    tornado.ioloop.IOLoop.instance().start()

