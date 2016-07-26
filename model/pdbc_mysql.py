# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-25 14:03:25
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-26 15:37:35
import sys
sys.path.append('..')

from sqlobject import *
from config import Config

def mysql_init():
    host = Config.mysql.host
    port = Config.mysql.port
    pwd = Config.mysql.pwd

    sqlhub.processConnection = connectionForURI('mysql://{user}:{pwd}@{host}:{port}/vmts'.format(user='root', pwd=pwd, host=host, port=port))

class User(SQLObject):
    ''''''

    user = StringCol(length=120, notNone=True)
    passwd = StringCol(length=120)
    description = StringCol(length=20)
    email = StringCol(length=120)
    last_login = DateTimeCol()




if __name__ == '__main__':
    mysql_init()
    if not User.tableExists():
        User.createTable()
        print User.createTableSQL()