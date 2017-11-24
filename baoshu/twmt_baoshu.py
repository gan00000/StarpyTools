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

def getServerRealTime(login_headers,login_session):

    today = time_helper.get_current_time()
    # http: // mthxtw.gm.starpytw.com / Stat / realTime
    postRealTimeUrl = 'http://mthxtw.gm.starpytw.com/Stat/realTime'

    postVaule = {
        'server_id': '1001',
        'platform_id': '1'
    }

    contentPage = login_session.post(postRealTimeUrl, data=postVaule, headers=login_headers)
    # print contentPage.text

    soup_s_data = BeautifulSoup(contentPage.content, 'html.parser')

    # serverList = soup_s_data.find_all('select', name_="server_id")
    # if serverList[0]:
    #     servers = serverList[0].find_all('option')
    #     if servers:
    #         for s in servers:
    #             print s.string

    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    realTimeInfo = soup_s_data.tbody

    tdlist = realTimeInfo.find_all('td')
    sMsg = ServerMsg()

    if tdlist:
        sMsg.newRole = tdlist[1].string
        sMsg.roleLogin = tdlist[2].string

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
        sMsg.serverName = u'S1-隱秘之森'
        # td_string = tdlist.string
        # print td_string
        return sMsg


    # print realTimeInfo
    return None

def getServerAllPay(login_session,sMsg,serverId):

    mValues = {
        'serverid': serverId
    }
    result = login_session.post('http://sd.q5.com/index.php/main/sel_server', data=mValues)

    today = time_helper.get_current_time()
    startDay='2017-08-12'
    url = 'http://sd.q5.com/index.php/functionlist/game_func/93?start=' + startDay + '&end=' + today + '&serverid=0&paytype=1'

    contentPage = login_session.get(url)
    soup_pay_data = BeautifulSoup(contentPage.content, 'html.parser')

    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    servers_pay_info_array = soup_pay_data.find_all('table', id='table_charta')
    if servers_pay_info_array:
        pay_info = servers_pay_info_array[0]
        trlist = pay_info.find_all('tr')
        trlist.pop(0)
        mTotalPay = 0
        for tr in trlist:
            if tr:
                td_lsit = tr.find_all('td')
                total_pay = td_lsit[4].string
                if total_pay:
                    mTotalPay = mTotalPay + round(float(total_pay)/100, 2)

        return mTotalPay


def getServerAllReg(login_session,sMsg,serverId):
    # http://sd.q5.com/index.php/functionlist/game_func/106

    today = time_helper.get_current_time()
    startDay = '2017-08-12'
    url = 'http://sd.q5.com/index.php/functionlist/game_func/106?start=' + startDay + '&end=' + today + '&serverid=0'
    contentPage = login_session.get(url)

    soup_reg_data = BeautifulSoup(contentPage.content, 'html.parser')

    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    servers_reg_info_array = soup_reg_data.find_all('table', id='table_charta')
    if servers_reg_info_array:
        reg_info = servers_reg_info_array[0]
        trlist = reg_info.find_all('tr')
        trlist.pop(0)
        mTotalReg = 0
        for tr in trlist:
            if tr:
                td_lsit = tr.find_all('td')
                total_reg = td_lsit[5].string
                if total_reg:
                    mTotalReg = mTotalReg + int(total_reg)
        return mTotalReg



def getServerPayData(login_session,sMsg,serverId):

    mValues = {
        'serverid': serverId
    }
    result = login_session.post('http://sd.q5.com/index.php/main/sel_server', data=mValues)

    today = time_helper.get_current_time()
    url = 'http://sd.q5.com/index.php/functionlist/game_func/93?start=' + today + '&end=' + today + '&serverid=0&paytype=1'

    contentPage = login_session.get(url)
    soup_pay_data = BeautifulSoup(contentPage.content, 'html.parser')

    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    servers_pay_info_array = soup_pay_data.find_all('table', id='table_charta')
    if servers_pay_info_array:
        pay_info = servers_pay_info_array[0]
        trlist = pay_info.find_all('tr')
        tr = trlist[1]
        if tr:
            td_lsit = tr.find_all('td')

            sMsg.data = td_lsit[0].string
            sMsg.roleLogin = td_lsit[1].string

            sMsg.totalRolePay = 0
            payRoleCount = td_lsit[2].string
            if payRoleCount:
                payRoleCount_int = int(payRoleCount)
                sMsg.totalRolePay = payRoleCount_int
            sMsg.totalPay = 0
            total_pay = td_lsit[4].string
            if total_pay:
                sMsg.totalPay = round(float(total_pay)/100, 2)
                if sMsg.totalRolePay >0:
                    sMsg.arppu = round(sMsg.totalPay/sMsg.totalRolePay,2)
            sMsg.payPercent = td_lsit[5].string

            sMsg.newRole = td_lsit[10].string
            sMsg.newPayRole = td_lsit[11].string
            sMsg.newPay = td_lsit[12].string


def getAllDataMTHX():
    headers, login_session = loginTWMT()

    sMsg_array = []
    sMsg = getServerRealTime(headers, login_session)
    if sMsg:
        sMsg_array.append(sMsg)

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
        writeExcelForGameInfo('E:\\jingling\\mthx_baoshu.xls', u'魔塔Online %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))), listSmsg)

if __name__ == '__main__':
    getAllDataMTHX()