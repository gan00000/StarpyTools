# -*- coding: utf-8 -*-

import logging

from apscheduler.schedulers.background import BlockingScheduler

from baoshu import hajl, ahdl_baoshu, twzj_baoshu, gbzj_baoshu
from baoshu.bmdzz import *
from baoshu.gbml_baoshu import getGbmlAll
from baoshu.twmt_baoshu import getAllDataMTHX
from plugins.baobiao import pachonggl
from plugins.baobiao.pachong import *

logging.basicConfig()


def myJob():

    # for a in range(2):
    # try:
    #     getGameDataInfoBean()
    # except Exception, e:
    #     print 'error message:', e.message

    try:
        bmdzzbaoshu()
    except Exception, e:
        print 'error message:', e.message

    # try:
    #
    #     hajl.requestData()
    # except Exception, e:
    #     print 'error message:', e.message
    try:

        pachonggl.getGameDataInfoBeanGl()
    except Exception, e:
        print 'error message:', e.message

    try:

        ahdl_baoshu.getAhdlData()
    except Exception, e:
        print 'error message:', e.message

    # try:
    #     qmah_baoshu.getAllDataQmah()
    # except Exception, e:
    #     print 'error message:', e.message

    try:
        getAllDataMTHX()
    except Exception, e:
        print 'error message:', e.message

    try:
        twzj_baoshu.getAllDataTWZJ()
    except Exception, e:
        print 'error message:', e.message

    try:
        getGbmlAll()
    except Exception, e:
        print 'error message:', e.message

    try:
        gbzj_baoshu.getAllDataGBZJ()
    except Exception, e:
        print 'error message:', e.message

    print '---------------------read data finish---------------------'
    path_m = 'E:\\pachongmsg.txt'

    f_f = open(path_m, 'w')
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    f_f.write(t)
    f_f.close()
    
    print '---------------------write pachongmsg data finish---------------------'


if __name__ == '__main__':

    sched = BlockingScheduler()
    sched.add_job(myJob, 'cron', max_instances=10, hour='1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23', minute='54')
    # sched.add_job(myJob, 'interval', hours=1)
    # sched.add_job(myJob, 'interval', hours=1,start_date=0)
    try:
        myJob()
        sched.start()
    except Exception, e:
        print 'e.message:\t', e.message
        pass



