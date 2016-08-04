# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-22 15:35:58
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-22 15:36:15

import sys
sys.path.append('..')

from redisco import models, connection_setup
from config import Config

def redis_init(db=0):
    host = Config.redis.host
    port = Config.redis.port
    pwd = Config.redis.pwd

    connection_setup(host=host, port=port, password=pwd, db=db)


class UserInterface(models.Model):
    ''''''

    id = models.IntegerField(required=True, unique=True)
    user = models.Attribute(required=True, unique=True)
    pwd = models.Attribute()
    description = models.Attribute()
    email = models.Attribute()
    avatar = models.Attribute()
    last_login = models.DateTimeField(auto_now=True)

class TestSuit_Maintaince(models.Model):
    ''''''

    id = models.Counter(required=True, unique=True)
    overview = models.Attribute(required=True)
    target = models.Attribute(required=True)
    status = models.Attribute(required=True)
    detail = models.ListField(dict)

class DeviceInfoInterface(models.Model):
    ''''''

    timestamp = models.DateTimeField(required=True)
    cpu_usage = models.Attribute()
    mem_usage = models.Attribute()
    net_usage = models.Attribute()
    net_flow = models.ListField(dict)
    proc_info = models.ListField(dict)

class DeviceInterface(models.Model):
    ''''''

    dev_ip = models.Attribute(required=True)
    timestamp = models.DateTimeField(required=True)
    status = models.Attribute(required=True)
    static_info = models.ListField(dict, required=False)
    dynamic_info = models.ListField(DeviceInfoInterface, required=False)

class DeviceInfoPeriodInterface(models.Model):
    ''''''

    dev_id = models.Attribute(required=True, unique=True)
    dynamic_period_info = models.ListField(DeviceInfoInterface)


redis_init()

if __name__ == "__main__":

    #user = UserInterface(id=11, user='reimu', pwd='reimu', description='楽園の巫女', avatar='Reimu2.jpg')
    #print user.is_valid()
    #print user.save()
    #print UserInterface.objects.all()
    a = UserInterface.objects.filter(user='reimu')
    print a
    print type(a)
    print a[0].pwd