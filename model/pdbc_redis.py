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

    dev_id = models.Attribute(required=True, unique=True)
    ip = models.Attribute(required=True)
    type = models.Attribute(required=True)
    name = models.Attribute(required=True)
    status = models.Attribute(required=True)
    static_info = models.ListField(dict, required=False)
    service_status = models.ListField(dict)

class DeviceDynamicInterface(models.Model):
    ''''''
    dev_id = models.Atrribute(required=True)
    timestamp = models.DateTimeField(required=True)

    dynamic_info = models.ListField(DeviceInfoInterface, required=False)


redis_init()

if __name__ == "__main__":
    import datetime
    import time
    user = UserInterface(id=11, user='reimu', pwd='reimu', description='楽園の巫女', avatar='Reimu2.jpg')
    print user.is_valid()
    print user.save()
    #print UserInterface.objects.all()
    #b = DeviceInterface(dev_ip='192.168.5.109', timestamp=datetime.datetime.now(), status='1')
    #a = UserInterface.objects.filter(user='reimu')
    #print a
    #print type(a)
    #print a[0].pwd
    #print b.is_valid()
    #print b.save()
    #t1 = time.time()
    #print DeviceInterface.objects.filter(dev_ip='192.168.5.109')
    #for i in DeviceInterface.objects.all():
    #    print i
    #print time.time() - t1