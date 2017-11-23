# -*- coding: utf-8 -*-
from datetime import datetime

from baoshu import hajl, ahdl_baoshu, qmah_baoshu
from plugins.baobiao import pachonggl
from plugins.baobiao.pachong import *
from apscheduler.schedulers.background import BlockingScheduler
from baoshu.bmdzz import *
import logging
logging.basicConfig()
import requests

def myJob():

    try:
        r = requests.get("http://www.yor88.com/mnt/kb.txt")
        if r:
            print r.content
            path_m = 'E:\\kbmessage.txt'
            f_f = open(path_m, 'w')
            f_f.write(r.content)
            f_f.close()


    except Exception, e:
        print 'error message:', e.message



if __name__ == '__main__':

    sched = BlockingScheduler()
    sched.add_job(myJob, 'cron', max_instances=10, hour='7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23', minute='5')
    # sched.add_job(myJob, 'interval', hours=1)
    # sched.add_job(myJob, 'interval', hours=1,start_date=0)
    try:
        myJob()
        sched.start()
    except Exception, e:
        print 'e.message:\t', e.message
        pass



