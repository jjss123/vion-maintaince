# -*- coding: utf-8 -*-
# @Author: hylide
# @Date:   2016-07-21 16:43:41
# @Last Modified by:   hylide
# @Last Modified time: 2016-07-21 16:43:55

import os
import re
import time

def get_pid_list():
    pid = []
    for d in os.listdir('/proc'):
        if re.match(r'^\d*$', d):
            pid.append(d)

    return pid

def all_proc_detail():
    pass

def resolve_status():
    pass


if __name__ == "__main__":
    t1 = time.time()
    print get_pid_list()
    print time.time() - t1