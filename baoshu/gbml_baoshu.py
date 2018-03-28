# -*- coding: UTF-8 -*-
import json

import requests
import os

import time

from baoshu.ServerMsg import ServerMsg
from baoshu.smsgtool import sumSmsg
from baoshu.time_helper import get_current_time2
from excel.excelutil import writeExcelForGameInfo


def getGbmlAll():
    url = 'http://manager.starpyse.com/fn/data/report?gameCode=gbml&aa=' + get_current_time2()
    res = requests.get(url)
    print res.text

    if res:
        res_json = json.loads(res.text)
        array_s = res_json.get('topup')
        loginNum = res_json.get('loginNum')
        print(loginNum)
        if array_s:
            s_info_list = []
            for i in range(len(array_s)):
                s_obj = array_s[i]

                sm = ServerMsg()
                price = s_obj.get('price')
                serverName = s_obj.get('serverName')
                peopleNum = s_obj.get('peopleNum')
                print(str(price) + "  " + serverName + "  " + str(peopleNum))
                sm.serverName = serverName
                sm.totalPay = price
                sm.totalRolePay = peopleNum

                if i == 0:
                    sm.roleLogin = loginNum

                s_info_list.append(sm)
            listSmsg = sumSmsg(s_info_list)
            writeExcelForGameInfo('E:\\jingling\\gbml_baoshu.xls',
                                  u'魔龍 %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))),
                                  listSmsg)


if __name__ == '__main__':
    getGbmlAll()
