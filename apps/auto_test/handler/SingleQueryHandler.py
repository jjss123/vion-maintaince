# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-10-24 11:26:15
# @Last Modified by:   hylide
# @Last Modified time: 2016-10-24 11:26:36

import tornado.web

from apps.auto_test.libs.envelope import soap_request

class SingleQueryHandler(tornado.web.RequestHandler):

    def post(self):
        '''
        recv post msg, params:
         "url","method", "params"
        '''
        self.url = self.get_argument('url')
        self.method = self.get_argument('method')
        try:
            self.params = self.get_argument('params')
            (head, data) = soap_request(self.url, self.method, self.params)
        except tornado.web.MissingArgumentError:
            (head, data) = soap_request(self.url, self.method)

        client = tornado.httpclient.HTTPClient()
        self.response = client.fetch(self.url, data, method='POST')
        return self.response