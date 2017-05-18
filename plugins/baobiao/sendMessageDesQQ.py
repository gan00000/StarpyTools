# -*- coding: utf-8 -*-
from datetime import datetime
from plugins.baobiao.pachong import *
from apscheduler.schedulers.background import BlockingScheduler
from baoshu.bmdzz import *

def myJob():
    try:
        s1, s2, s3, s4 = getGameAllInfo()
        t = time.strftime('%Y-%m-%d %H:%M')
        s_time = t + ' 数据:\n\n'

        s = s_time + s1 + '\n' + s2 + '\n' + s3 + '\n\n' + s4

        print s

        bmdzz_info = bmdzzbaoshu()
        s  = s + '\n\n' + bmdzz_info

        path_m = 'E:\\pachongmsg.txt'
        if os.path.exists(path_m):
            f_f = open(path_m, 'w')
            f_f.write(s)
            f_f.close()
    except:
        pass

if __name__ == '__main__':

    sched = BlockingScheduler()
    sched.add_job(myJob, 'cron', hour='7,9,11,13,15,17,18,19,20,21,22,23', minute='54')
    try:
        # myJob()
        sched.start()
    except:
        pass



