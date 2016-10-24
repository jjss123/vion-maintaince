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

with open(CONFIG) as file:
    Config = DictObject(json.loads(file.read()))
with open(ROUTE) as file:
    Route = DictObject(json.loads(file.read()))

def get_config(module):
    return Config.__getattribute__(module)

