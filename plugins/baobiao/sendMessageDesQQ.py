# -*- coding: utf-8 -*-
from datetime import datetime
from plugins.baobiao.pachong import *
from apscheduler.schedulers.background import BlockingScheduler
from baoshu.bmdzz import *
import logging
logging.basicConfig()

def myJob():
    try:
        # s1, s2, s3, s4 = getGameAllInfo()
        # t = time.strftime('%Y-%m-%d %H:%M')
        # s_time = t + ' 数据:\n\n'
        #
        # s = s_time + s1 + '\n' + s2 + '\n' + s3 + '\n\n' + s4
        #
        # bmdzz_info = bmdzzbaoshu()
        # s = s + '\n\n' + bmdzz_info
        # print s
        # path_m = 'E:\\pachongmsg.txt'
        # if os.path.exists(path_m):
        #     f_f = open(path_m, 'w')
        #     f_f.write(s)
        #     f_f.close()

        getGameDataInfoBean()
        bmdzzbaoshu()
        path_m = 'E:\\pachongmsg.txt'
        if os.path.exists(path_m):
            f_f = open(path_m, 'w')
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            f_f.write(t)
            f_f.close()
    except:
        pass

def testJob():
    print 'test job'

if __name__ == '__main__':

    sched = BlockingScheduler()
    sched.add_job(myJob, 'cron', hour='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23', minute='58')
    # sched.add_job(myJob, 'interval', hours=1)
    # sched.add_job(myJob, 'interval', hours=1,start_date=0)
    try:
        myJob()
        sched.start()
    except Exception, e:
        print 'e.message:\t', e.message
        pass



