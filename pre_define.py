# -*- coding: utf-8 -*-
# @Author: riposa
# @Date:   2016-06-12 10:08:06
# @Last Modified by:   riposa
# @Last Modified time: 2016-07-12 16:23:57
"""
error code:
    0x00, the leaf_name didnt match with leaves-node Index(self.index)
    0x01,
"""

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


class Node(object):

    def __init__(self, child=None, name=None, value=None, isLeaf=False):
        if child is not None:
            self._check_child(child)

        self.__child = self.add_child(child)
        self.name = name
        self.isLeaf = isLeaf
        if not self.isLeaf and value:
            raise ValueError('Only leaf node own its value.')
        self.value = value


    def _check_child(self, child):
        if type(child) == list:
            if False in set([isinstance(i, Node) for i in child]):
                raise ValueError('child node must be an instance of Node class.')
        elif not isinstance(child, Node):
            raise ValueError('child node must be an instance of Node class.')

        return type(child)

    def add_child(self, child_node):

        if child_node is not None:
            child_type =  self._check_child(child_node)
        else:
            raise ValueError('child node must not be None.')

        if child_type == list:
            self.__child.extend(child_node)
        elif child_type == object:
            self.__child.append(child_node)


class DictTrie(object):
    """
    Trie-tree class for loading all the config
    """

    def __init__(self):

        self.root = Node(name='vmts-root')
        self.index = dict()

    def append_child(self, dictObj, root_node=None):
        """
        :param dictObj: new dictobj for extend dict-trie tree.
        :param root_node: the root node you wanna to make new dictobj append on,
        :return: None
        """

        if root_node is None:
            root = self.root
        else:
            root = root_node


        def create_node(dictObj, root):

            for i in dictObj:
                n = Node(name=i)
                root.add_child(n)
                if type(dictObj[i]) == dict:
                    create_node(dictObj=dictObj[i], root=n)
                elif type(dictObj[i]) == list:
                    trans_dict = {}
                    for k in range(len(dictObj[i])):
                        trans_dict[k] = dictObj[i][k]
                    create_node(dictObj=dictObj[i], root=n)
                else:
                    n.isLeaf = True
                    n.value = dictObj[i]
                    self.index[n.name] = n

        create_node(dictObj=dictObj, root=root)


    def get(self, leaf_name):
        """
        :param leaf_name: <str> or <int>, the leaf-node config name.
        :return: <tuple>, (result, msg)
                success: <boolean>, the result of trying to get the config value,
                msg: if success is true, msg means the value of the config name,
                     if is false, means the error code of reason.
        """

        if leaf_name not in self.index:
            return 0x00













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
