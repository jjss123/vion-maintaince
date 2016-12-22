# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-10-24 11:26:15
# @Last Modified by:   hylide
# @Last Modified time: 2016-10-24 11:26:36

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


if __name__ == '__main__':
    import time

    test = {
        "a": 1,
        "b":{
            "c": 2,
            "d": {
                "e": 3,
                "f": [1,2,4],
                "g": {
                    "h":55
                }
            }
        }
    }
    t1 = float(time.time())
    test_obj = DictObject(test)
    t2 = float(time.time())
    print test_obj
    print test_obj.a

    print test_obj.b.c
    print test_obj.b.d
    t3 = time.time()
    print test_obj.b.d.e
    t4 = time.time()
    test_obj.b.d.e = '1'
    t5 = time.time()
    print 'init time: ', t2-t1
    print 'call time: ', t4-t3
    print 'set time: ', t5-t4

