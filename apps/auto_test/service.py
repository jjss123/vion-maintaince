# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen

import urllib
import json
import time
from envelope import soap_request, resolve_post
from tornado.options import define, options
define("port", default=8192, help="run on the given port", type=int)

ip = '192.168.9.106'
url = 'http://192.168.9.106:10030/'
method_name = 'GetDeviceInfo'
param = {'deviceSerialNums': '00-10-14-87-cd-a1', 'nDeviceInfoType': '0', 'bGroup': 'false'}

def cost():


@cost
def soap_send(url, data):
	client = tornado.httpclient.HTTPClient()
	response = client.fetch(url, method='POST', data)
	return response

class IndexHandler(tornado.web.RequestHandler):

	def get(self):
		self.req = []
		for wsnp in self._get_argument("wsnp"):
			self.req.append(wsnp)

		length = len(self.req)
		i = 0
		while i < length:
			wsnp = self.req[i]
			(head, data) = soap_request(wsnp.host, wsnp.svr, wsnp.params)
			soap_send(wsnp.url, wsnp.data)






	def GetDeviceInfo():
		(head, data) = soap_request(ip, 'GetDeviceInfo', {'deviceSerialNums': '00-10-14-87-cd-a1', 'nDeviceInfoType': '0', 'bGroup': 'false'})
		client = tornado.httpclient.HTTPClient()
		response = client.fetch(url, method = 'POST', body = data)
		print response.body

	def GetVersion():
		(head, data) = soap_request(ip, 'GetVersion')
		client = tornado.httpclient.HTTPClient()
		response = client.fetch(url, method = 'POST', body = data)
		print response.body

	def ExportConfigs():
		(head, data) = soap_request(ip, 'ExportConfigs',{'deviceSerialNums': '00-10-14-87-cd-a1', 'configName': 'ServerConfig', 'softServiceName': 'QServer'})
		client = tornado.httpclient.HTTPClient()
		response = client.fetch(url, method = 'POST', body = data)
		print response.body


if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
