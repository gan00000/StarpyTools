# -*- coding: utf-8 -*-
from datetime import datetime

from qqbot import QQBotSched as qqbotsched, RunBot
from plugins.baobiao.pachong import *

# from qqbot.utf8logger import INFO

#@qqbotsched(second='5-55/5')
#def mytask(bot):
#    INFO('SCHEDULED')

@qqbotsched(hour='0,7,9,11,13,15,17,19,21,10', minute='05')
def mytask(bot):
    # cl = bot.List('buddy', '3497303033')
    # if cl:
    #     bot.SendTo(cl[0], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        s1,s2,s3,s4 = getGameAllInfo()
        gl = bot.List('group', '35186463')
        if gl is not None:
            for group in gl:
                bot.SendTo(group, s1)
                time.sleep(2)
                bot.SendTo(group, s2)
                time.sleep(2)
                bot.SendTo(group, s3)
                time.sleep(2)
                bot.SendTo(group, s4)
        # print s4

        # bs = bot.List('buddy')
        # if bs is not None:
        #     for b in bs:
        #         if b.qq == '372129081':
        #             bot.SendTo(b, s3)
        #             return

    except:
        pass
if __name__ == '__main__':
    RunBot()
