# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-25 14:24:26
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-25 15:15:06
import sys

import tornado.web
sys.path.append('..\\..')
from model import pdbc_mysql
from model import pdbc_redis

__all__ = ["MainPageHandler", "TestSuitHandler", "LoginHandler", "LogoutHandler"]

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainPageHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/")
            return
        user = self.get_secure_cookie("user")
        user_res = pdbc_redis.UserInterface.objects.filter(user=user)
        if user_res:
            self.render(
                "dashboard.html",
                User=user_res[0].user,
                comment=user_res[0].description,
                avatar=user_res[0].avatar
            )
        else:
            self.redirect("/")

class TestSuitHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/")
            return
        suit = self.get_argument('suit')
        user = self.get_secure_cookie("user")
        user_res = pdbc_redis.UserInterface.objects.filter(user=user)
        if user_res:
            self.render(
                "testsuit-{branch}.html".format(branch=suit),
                User=user_res[0].user,
                comment=user_res[0].description,
                avatar=user_res[0].avatar
                )
        else:
            self.redirect("/")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        user = self.get_argument("user")
        pwd = self.get_argument("password")

        res = pdbc_redis.UserInterface.objects.filter(user=user)
        if res:

            if user == res[0].user and pwd == res[0].pwd:

                self.set_secure_cookie("user", self.get_argument("user"), expires_days=1)
                self.write({"res":"success", "redirect":"/"})
            else:
                self.write({"res":"error","msg":"Invalid username or password"})

        else:
            self.write({"res":"error", "msg":"Non-existent user"})

class LogoutHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/")
            return
        self.set_secure_cookie("user", "")
        self.current_user = ''
        self.redirect("/login")

