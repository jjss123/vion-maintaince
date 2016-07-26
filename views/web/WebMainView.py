# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-25 14:24:26
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-25 15:15:06
import sys

import tornado.web
sys.path.append('..')
from model import pdbc_mysql
#from model import pdbc_redis

__all__ = ["MainPageHandler", "TestSuitHandler"]

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        pass

class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("dashboard.html",User='Cirno', comment='baka')

class TestSuitHandler(tornado.web.RequestHandler):
    def get(self):
        suit = self.get_argument('suit')
        if suit == 'maintaince':
            self.render("testsuit-maintaince.html",User='Cirno', comment='baka')

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")
