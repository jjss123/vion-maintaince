# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-22 15:38:14
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-22 15:38:26

import json
import os
from lib.dict_objectified import DictObject

CONFIG = '{path}/vmts.conf.json'.format(path=os.path.split(os.path.realpath(__file__))[0])
ROUTE = '{path}/vmts.route.json'.format(path=os.path.split(os.path.realpath(__file__))[0])
APPS = '{path}/apps/apps.conf.json'.format(path=os.path.split(os.path.realpath(__file__))[0])

CONFIG_ARRAY = {
    "config": CONFIG,
    "route": ROUTE,
    "apps": APPS
}

with open(CONFIG) as file:
    config = DictObject(json.loads(file.read()))
with open(ROUTE) as file:
    route = DictObject(json.loads(file.read()))
with open(APPS) as file:
    apps = DictObject(json.loads(file.read()))

def reload(moudle):
    with open(CONFIG_ARRAY[str(moudle).lower()]) as file:
        moudle = DictObject(json.loads(file.read()))
    return 0

def update(moudle, **dic):
    pass

