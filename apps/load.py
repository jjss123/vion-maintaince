# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-10-24 11:22:46
# @Last Modified by:   hylide
# @Last Modified time: 2016-10-24 11:24:08

import sys
import json
import os
sys.path.append('../')

from lib.dict_objectified import DictObject

with open("apps.conf.json") as file:
    conf = DictObject(json.loads(file.read()))

def load():
    pass