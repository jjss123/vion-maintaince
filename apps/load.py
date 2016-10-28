# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-10-24 11:22:46
# @Last Modified by:   hylide
# @Last Modified time: 2016-10-24 11:24:08

import sys
import json
import multiprocessing
sys.path.append('../')

from lib.dict_objectified import DictObject, Apps



def app_run(p):
    impstring = "from {app}.app import loading".format(app=p["app"])
    exec impstring

    loading(host=p["host"], port=p["port"], route=p["route"])


def load():
    app_list = Apps.apps
    proc = list()
    for i in app_list:
        if i.load:
            sub_proc = multiprocessing.Process(
                target=app_run,
                args={
                    "app":i.app,
                    "host": i.host,
                    "port": i.port,
                    "route": i.route
                })
            if i.load_type.lower() == "immediately":
                sub_proc.start()
            #todo: elif "delay"
            else:
                #todo: external
                pass

            proc.append(sub_proc)

    # all subprocess begin
    for i in proc:
        i.join()

def reload(**new_conf):
    with open("apps.conf.json") as file:
        conf = DictObject(json.loads(file.read()))