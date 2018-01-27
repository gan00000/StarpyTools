#-*- coding: UTF-8 -*-
import sys
import time
import types
from bs4 import BeautifulSoup

from baoshu import time_helper
from baoshu.AccountLogin import Login
from baoshu.ServerMsg import ServerMsg
from baoshu.smsgtool import sumSmsg
from excel.excelutil import writeExcelForGameInfo


def loginAhdl():
    mLogin = Login()
    loginPage = 'http://ahdltw-serlist.starb168.com:8188/longshuai/index'
    loginPostUrl = 'http://ahdltw-serlist.starb168.com:8188/longshuai/doLogin'
    postVaule = {
        'username': 'aliyouout',
        'password': 'aliyououtSD_'
    }
    headers = {
        'Host': 'ahdltw-serlist.starb168.com:8188',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    # menupage,urllib2 = userlogin.login(loginPostUrl,postVaule,headers,'hajj_cookies')
    login_success_page, login_session = mLogin.session_login(loginPage, loginPostUrl, postVaule, headers, 'ahdl_cookies')
    mainPage = login_session.get('http://ahdltw-serlist.starb168.com:8188/longshuai/index', headers=headers)

    return headers, login_session

def getAhdlData():

    helders,login_session = loginAhdl()
    servers_map = getServersMap(login_session) #获取所有服务器idhe名称

    sMsgArray_Android = getSMsgList(login_session, servers_map,'50100')#android
    sMsgArray_Ios = getSMsgList(login_session, servers_map,'50103')#IOS

    for smAndroid in sMsgArray_Android:
        for smIos in sMsgArray_Ios:
            if smAndroid.serverName == smIos.serverName:
                smAndroid.roleLogin = smAndroid.roleLogin + smIos.roleLogin
                smAndroid.newRole = smAndroid.newRole + smIos.newRole
                smAndroid.totalPay = smAndroid.totalPay + smIos.totalPay
                smAndroid.totalRolePay = smAndroid.totalRolePay + smIos.totalRolePay
                # smAndroid.totalRolePay = smAndroid.totalRolePay + smIos.totalRolePay

                if smAndroid.totalRolePay > 0:
                    smAndroid.arppu = round(smAndroid.totalPay / smAndroid.totalRolePay, 2)
                if smAndroid.roleLogin > 0:
                    smAndroid.payPercent = str(round((smAndroid.totalRolePay / float(smAndroid.roleLogin)) * 100, 2)) + '%'

    listSmsg = sumSmsg(sMsgArray_Android)
    writeExcelForGameInfo('E:\\jingling\\ahdl_baoshu.xls', u'暗黑邊境 %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))), listSmsg)


def getSMsgList(login_session, servers_map, channelId):
    sMsg_lsit = []
    for sId, sName in servers_map.items():

        print 'sId:' + sId + "  sName:" + sName
        mHeaders = {
            'Referer': 'http://ahdltw-serlist.starb168.com:8188/longshuai/payment/payment-synopsis-statistics'
        }
        mValues = {
            'serverId': sId,
            'channelId': channelId,
            'startDate': time_helper.get_current_time(),
            'endDate': time_helper.get_tomorrow_time()
        }
        serverData = login_session.post(
            'http://ahdltw-serlist.starb168.com:8188/longshuai/payment/payment-synopsis-statistics', headers=mHeaders,
            data=mValues)
        if serverData:
            # print serverData.text
            pageText = serverData.text
            # pageText = pageText.replace('\n','')
            soup_s_data = BeautifulSoup(pageText, 'html.parser')
            if soup_s_data:
                tr_list = soup_s_data.find_all('tr')
                sMsg = ServerMsg()

                mTr = tr_list[len(tr_list) - 1]
                tds = mTr.contents
                if tds:
                    mSname = tds[3].string
                    if mSname == None:
                        continue
                    for td in tds:
                        sMsg.data = tds[1].string
                        sMsg.gameName = '暗黑边境'
                        sMsg.serverName = mSname
                        payment = float(tds[9].string)

                        sMsg.totalPay = 0
                        if payment > 0:
                            payment = round(payment / 32, 2)
                            sMsg.totalPay = payment

                        sMsg.totalRolePay = 0
                        sMsg.roleLogin = 0

                        sMsg.roleLogin = int(tds[21].string)
                        sMsg.newRole = int(tds[15].string)
                        sMsg.totalRolePay = int(tds[7].string)

                        # sMsg.payPercent = tds[19]
                        print td.string
                    sMsg_lsit.append(sMsg)

                # for tr in tr_list:

                if channelId == '50100' and sMsg:
                    payment_1, newRole_1 = getSMsgLTVData(login_session,sId,'50100')
                    payment_2, newRole_2 = getSMsgLTVData(login_session,sId,'50103')
                    if (newRole_1 + newRole_2) > 0:
                        ltv = round((payment_1 + payment_2) / (newRole_1 + newRole_2), 2)
                        sMsg.ltv = ltv

    return sMsg_lsit


def getSMsgLTVData(login_session, sId, channelId):

    mHeaders = {
        'Referer': 'http://ahdltw-serlist.starb168.com:8188/longshuai/payment/payment-synopsis-statistics'
    }
    mValues = {
        'serverId': sId,
        'channelId': channelId,
        'startDate': '2017-07-29',
        'endDate': time_helper.get_tomorrow_time()
    }
    serverData = login_session.post(
        'http://ahdltw-serlist.starb168.com:8188/longshuai/payment/payment-synopsis-statistics', headers=mHeaders,
        data=mValues)
    if serverData:
        # print serverData.text
        pageText = serverData.text
        # pageText = pageText.replace('\n','')
        soup_s_data = BeautifulSoup(pageText, 'html.parser')
        if soup_s_data:
            tr_list = soup_s_data.find_all('tr')
            for tr in tr_list:
                tds = tr.contents
                if tds:
                    theServerMsgAllText = tds[1].string
                    if theServerMsgAllText == u'总计':
                        payment = float(tds[9].string)

                        payment = round(payment / 32, 2)
                        newRole = int(tds[15].string)
                        return payment, newRole
    return 0,0

def getServersMap(login_session):
    mHeaders = {
        'Referer': 'http://ahdltw-serlist.starb168.com:8188/longshuai/index',
    }
    payment_synopsis_statistics = login_session.get(
        'http://ahdltw-serlist.starb168.com:8188/longshuai/payment/payment-synopsis-statistics', headers=mHeaders)
    # print payment_synopsis_statistics.text
    servers_map = {}
    soup = BeautifulSoup(payment_synopsis_statistics.text, 'html.parser')
    servers_root = soup.find(name='option', text="全部服务器")
    servers = servers_root.find_next_siblings()
    for s in servers:
        s_id = s.get('value')
        s_text = s.string
        if s_id:
            servers_map[s_id] = s_text

    return servers_map


if __name__ == '__main__':
    getAhdlData()