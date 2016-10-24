# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-10-24 10:56:47
# @Last Modified by:   riposa
# @Last Modified time: 2016-10-24 10:56:56
import json

CFG = "service.config"

class DictObject(object):

    def __init__(self, dict_obj):
        keys = dict_obj.keys()
        for i in keys:
            if type(dict_obj[i]) == dict:
                self.__setattr__(i,  DictObject(dict_obj[i]))
            else:
                self.__setattr__(i, dict_obj[i])

    def __repr__(self):
        return self.__dictionary__()

    def __str__(self):
        return str(self.__repr__())

    def __getitem__(self, item):
        if isinstance(self.__getattribute__(item), DictObject):
            return self.__getattribute__(item).__str__()
        else:
            return self.__getattribute__(item)

    def __dictionary__(self):
        attr = self.__dict__
        for i in attr.keys():
            if isinstance(attr[i], DictObject):
                attr[i] = attr[i].__dictionary__()
        return attr

    def keys(self):
        return self.__dict__.keys()

    def has_key(self, key):
        if key in self.__dict__.keys():
            return True
        else:
            return False

def get():
    try:
        with open(CFG) as file:
            Config = DictObject(json.loads(file.read()))
            return Config
    except IOError:
        raise Exception("Configuration Missing!")