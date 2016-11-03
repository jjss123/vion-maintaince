# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-10-24 11:22:46
# @Last Modified by:   hylide
# @Last Modified time: 2016-10-24 11:24:08

import json

from config import apps
from lib.dict_objectified import DictObject

def app_run(app, host, port, route):
    impstring = "from {app}.app import launch".format(app=app)
    exec impstring

    launch(host, port, route)

def load():
    app_list = apps.apps
    proc = list()
    for i in app_list:
        i = DictObject(i)
        if i.load:
            app_run(i.app, )
            if i.load_type.lower() == "immediately":
                sub_proc.start()
            #todo: elif "delay"
            else:
                #todo: external
                pass

            print '\tapp: {app} loading ...'.format(app=i.app)
            proc.append(sub_proc)

    # all subprocess begin
    print 'all external apps loaded.'
    for i in proc:
        i.join()

def reload(**new_conf):
    with open("apps.conf.json") as file:
        conf = DictObject(json.loads(file.read()))