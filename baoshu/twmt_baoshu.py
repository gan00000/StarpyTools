#-*- coding: UTF-8 -*-
import simplejson as json
import re
import sys
import time
import types
from bs4 import BeautifulSoup

from baoshu.smsgtool import sumSmsg
from excel.excelutil import writeExcelForGameInfo

reload(sys)
sys.setdefaultencoding('utf-8')

from baoshu import time_helper
from baoshu.ServerMsg import ServerMsg
from baoshu.AccountLogin import Login


def loginTWMT():
    mLogin = Login()
    loginPage = 'http://mthxtw.gm.starpytw.com/Public/login'
    loginPostUrl = 'http://mthxtw.gm.starpytw.com/Public/signin'
    postVaule = {
        'username': 'kefu',
        'password': 'kefu'
    }
    headers = {
        'Referer': 'http://mthxtw.gm.starpytw.com/Public/login',
        'Host': 'mthxtw.gm.starpytw.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    # menupage,urllib2 = userlogin.login(loginPostUrl,postVaule,headers,'hajj_cookies')
    login_success_page, login_session = mLogin.session_login(loginPage, loginPostUrl, postVaule, headers, 'qmah_cookies')

    postVauleMMM = {
        'operator_id': '202'
    }
    login_session.post('http://mthxtw.gm.starpytw.com/Public/comfirmOperator',data=postVauleMMM)

    mainPage = login_session.get('http://mthxtw.gm.starpytw.com/Index/index', headers=headers)

    # print mainPage.text

    return headers, login_session

def getServerList(login_headers,login_session):
    realTimeUrl = 'http://mthxtw.gm.starpytw.com/Stat/realTime'

    contentPage = login_session.get(realTimeUrl)

    soup_s_data = BeautifulSoup(contentPage.content, 'html.parser')

    servers_list = []

    serverList = soup_s_data.find_all('select', attrs={"name": "server_id"})
    if serverList and serverList[0]:
        server_option_list = serverList[0].find_all('option')
        if server_option_list:  # 遍列服务器 id 和 名称
            for server_option in server_option_list:
                serverMsg = ServerMsg()
                print server_option['value']
                print server_option.string
                serverMsg.serverId = server_option['value']
                serverMsg.serverName = server_option.string
                servers_list.append(serverMsg)

    return servers_list

def getServerRealTime(login_headers,login_session, sMsg):

    today = time_helper.get_current_time()
    # http: // mthxtw.gm.starpytw.com / Stat / realTime
    postRealTimeUrl = 'http://mthxtw.gm.starpytw.com/Stat/realTime'

    postVaule = {
        'server_id': sMsg.serverId,
        'platform_id': '1'
    }

    contentPage = login_session.post(postRealTimeUrl, data=postVaule, headers=login_headers)
    # print contentPage.text

    soup_s_data = BeautifulSoup(contentPage.content, 'html.parser')


    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    realTimeInfo = soup_s_data.tbody

    tdlist = realTimeInfo.find_all('td')

    if tdlist:
        sMsg.newRole = tdlist[1].string
        sMsg.roleLogin = tdlist[2].string
        sMsg.allDayReg = int(tdlist[3].string)

        sMsg.totalPay = 0
        sMsg.totalPay = tdlist[4].string
        if sMsg.totalPay > 0:
            sMsg.totalPay = round(float(sMsg.totalPay) / 6.7, 2)

        sMsg.newPayRole = tdlist[7].string

        sMsg.totalRolePay = 0
        sMsg.totalRolePay = int(tdlist[6].string)
        if sMsg.totalRolePay > 0:
            sMsg.arppu = round(sMsg.totalPay / sMsg.totalRolePay, 2)

        sMsg.payPercent = tdlist[11].string
        sMsg.gameName = u'魔塔Online'
        # sMsg.serverName = u'S1-隱秘之森'
        # td_string = tdlist.string
        # print td_string
        return sMsg


    # print realTimeInfo
    return None

def getServerAllPay(login_headers,login_session, sMsg):


    today = time_helper.get_current_time_2()

    mValues = {
        'server_id': sMsg.serverId,
        'platform_id':'1',
        'date_range':'2017/11/23 - ' + today
    }
    result = login_session.post('http://mthxtw.gm.starpytw.com/Stat/basic', data=mValues, headers=login_headers)

    soup_pay_data = BeautifulSoup(result.content, 'html.parser')

    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    servers_pay_info_array = soup_pay_data.find_all('tr')
    if servers_pay_info_array:
        pay_info = servers_pay_info_array[len(servers_pay_info_array) - 1]
        tdlist = pay_info.find_all('td')
        all_pay = tdlist[6].string

        pays = round(float(all_pay) / 6.7, 2)  #历史储值（除了当天）
        print pays
        sMsg.allDayPay = pays + sMsg.totalPay  #总储值
        sMsg.ltv = round(sMsg.allDayPay / sMsg.allDayReg, 2)
        print sMsg.allDayPay




def getAllDataMTHX():
    headers, login_session = loginTWMT()

    sMsg_array = getServerList(headers, login_session)
    for sMsg in sMsg_array:
        s = getServerRealTime(headers, login_session, sMsg)
        getServerAllPay(headers, login_session, sMsg)


    # servers_map = getServerMap(headers,login_session)
    #
    # sMsg_array = []
    # for k,v in servers_map.items():
    #     if k == '0' or k == '999':
    #         continue
    #     sMsg = ServerMsg()
    #     sMsg.gameName = u'破战'
    #     sMsg.serverName = v
    #     try:
    #         getServer_ccu(login_session, sMsg, k)
    #     except:
    #         pass
    #     try:
    #         getServerPayData(login_session, sMsg, k)
    #     except:
    #         pass
    #     try:
    #        totalPay = getServerAllPay(login_session, sMsg, k)
    #        allReg = getServerAllReg(login_session, sMsg, k)
    #        if allReg:
    #            ltv = round(totalPay / allReg,2)
    #            sMsg.ltv = ltv
    #     except Exception, e:
    #         print 'error message:', e.message
    #         pass
    #     sMsg_array.append(sMsg)
    #
    if len(sMsg_array) > 0:
        listSmsg = sumSmsg(sMsg_array)
        # writeExcelForGameInfo('E:\\jingling\\mthx_baoshu.xls', u'魔塔Online %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))), listSmsg)

if __name__ == '__main__':
    getAllDataMTHX()