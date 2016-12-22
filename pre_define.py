# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 10:08:06
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:23:57

import json
import os

base_dir = os.path.dirname(__file__) + '../conf/'

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

class KeyValue(object):

    def __init__(self, key, value, depth, parentId):
        self.key = key
        self.value = value
        self.depth = depth
        self.parentId = parentId


@singleton
class GlobalVar(object):

    def __init__(self):
        self.config = dict()

    def list(self):
        """
        show current global variables
        :return: <dict>
        """
        res = dict()
        for i in dir(GlobalVar):
            if '::' in i:
                rg = i.split('::')[1]
                n = i.split('::')[0].split('__')[1]
                if res.has_key(rg):
                    res[rg][n] = GlobalVar.__getattribute__(i)
                else:
                    res[rg] = {n: GlobalVar.__getattribute__(i)}
        return res

    def set(self, key, value, region):
        """
        set global variables
        :param params: <dict>
        :param src: <str>
        :return: <Boolean>
        """
        try:
            def ret(p, s):
                for i in p.keys():
                    if type(p[i]) == dict:
                        ret(p[i], s + '.' + i)
                    setattr(GlobalVar, s + "." + i, p[i])
            ret(params, src)
            self.region.add(src)
        except:
            return False

        return True

    def get(self, key, region):
        """
        get global variables
        :param attrs:
        :return:
        """
        if not attrs:
            return self.list()

        res = {}
        for i in attrs:
            if not self.region:
                raise Exception('Region set has not been initialed.')
            for j in self.region:
                try:
                    tmp_res = GlobalVar.__getattribute__( i + '::' + j)
                except AttributeError:
                    continue
                if res.has_key(j):
                    res[j][i] = tmp_res
                else:
                    res[j] = {i:tmp_res}

        return res

    def load(self):
        for roots, dirs, files in os.walk(base_dir):
            for i in files:
                if os.path.splitext(i)[1] == '.json':
                    fn = os.path.splitext(i)[0]

                    with open(os.path.abspath(i)) as f:
                        fc = json.loads(f.read())



def load_config(input_dict):
    predef = GlobalVar()
    for i in input_dict:
        if type(input_dict[i]) == dict:
            predef.set()

if __name__ == '__main__':
    '''a = GlobalVar()
    print a.set({"test": 1, "tt": {"cc": 3}}, 'region1')
    a.set({"bbbb":33}, 'region2')
    a.set({"test":2}, 'region2')
    print dir(GlobalVar)
    print a.list()
    print a
    b = GlobalVar()
    print b.get("cc",'yy')'''

    t = {
        "a": 1,
        "b": {
            "c": 2,
            "d": {
                "e": 3,
                "f": [1, 2, 4],
                "g": {
                    "h": 55
                }
            }
        }
    }
    import time
    t1 = time.time()
    test = DictObjectTree(t, 'root')

    print test
    print test.root.child
