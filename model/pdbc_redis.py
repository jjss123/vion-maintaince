# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-22 15:35:58
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-22 15:36:15

import redis

import sys
sys.path.append('..')
from config import Config

__all__ = ["redis_init", "VmtsRedisModel"]

def redis_init(db=0):
    host = Config.redis.host
    port = Config.redis.port
    pwd = Config.redis.pwd

    return redis.Redis(host=host, port=port, password=pwd, db=db)


class VmtsRedisModel(object):
    ''''''

    def __init__(self, db=0):
        self.conn = redis_init(db)


    def


if __name__ == "__main__":
    rs = redis_init()
    print rs.get('test')