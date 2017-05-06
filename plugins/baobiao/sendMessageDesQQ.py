# -*- coding: utf-8 -*-
from datetime import datetime
from plugins.baobiao.pachong import *
from apscheduler.schedulers.background import BlockingScheduler


def myJob():
    try:
        s1, s2, s3, s4 = getGameAllInfo()
        t = time.strftime('%Y-%m-%d %H:%M')
        s_time = t + ' 数据:\n\n'

        s = s_time + s1 + '\n' + s2 + '\n' + s3 + '\n\n' + s4

        print s
        path_m = 'E:\\pachongmsg.txt'
        if os.path.exists(path_m):
            f_f = open(path_m, 'w')
            f_f.write(s)
            f_f.close()
    except:
        pass

if __name__ == '__main__':

    sched = BlockingScheduler()
    sched.add_job(myJob, 'cron', hour='7,9,11,13,15,17,19,21,23', minute=57)
    try:
        sched.start()
    except:
        pass



