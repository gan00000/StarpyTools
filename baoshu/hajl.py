#-*- coding: UTF-8 -*-
import os
import sys
import time
import types
import simplejson as json
import xlwt
from bs4 import BeautifulSoup

from baoshu.smsgtool import sumSmsg, doErrorMsg
from excel.excelutil import *
from time_helper import *
from ServerMsg import *

#解决 UnicodeDecodeError: 'ascii' codec can't decode 报错
from baoshu.AccountLogin import Login
from baoshu.Login2 import Login2

reload(sys)
sys.setdefaultencoding('utf8')


def requestData():
    mLogin = Login()
    loginPage = 'http://jllrcsss-tw.starb168.com/gameManager/index.jsp'
    loginPostUrl = 'http://jllrcsss-tw.starb168.com/gameManager/login.do'
    postVaule = {
        'username': 'csstarby3',
        'password': '123456'
    }
    headers = {
        'Referer': 'http://jllrcsss-tw.starb168.com/gameManager/index.jsp',
        'Host': 'jllrcsss-tw.starb168.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }

    # menupage,urllib2 = userlogin.login(loginPostUrl,postVaule,headers,'hajj_cookies')

    login_success_page, login_session = mLogin.session_login(loginPage, loginPostUrl, postVaule, headers, 'hajj_cookies')

    menupage = login_session.get('http://jllrcsss-tw.starb168.com/gameManager/menu.jsp', headers=headers)
    # print menupage.text
    #每个接口都需要 带这个 头header才能访问通过（奇怪）
    listSmsg = showDailyReport(login_session, headers)

    listSmsg = sumSmsg(listSmsg)

    writeExcelForGameInfo('E:\\jingling\\hajl_baoshu.xls',u'精灵王国 %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))),listSmsg)

    errorLogFile = 'E:\jingling\errorMsg\hajl_errorLog.txt'
    doErrorMsg(errorLogFile, listSmsg)
    return listSmsg


def showDailyReport(loginSession,headers):
    url = 'http://jllrcsss-tw.starb168.com/gameManager/view/pay/showDailyReport.jsp'
    loginSession.get(url, headers=headers)

    serverIds = getServers(headers, loginSession)#获取所有伺服器id
    allServersCurrentDayMsg = []
    startTime = get_current_time() + ' 00:00:00'
    if serverIds:
        print serverIds
        for sId in serverIds:
            print 'serverId:' + str(sId)
            #获取当天的服信息
            currentDaySmsgArray = getServerMsg(headers, loginSession, sId, startTime)  # 获取当天该伺服器信息
            if currentDaySmsgArray and len(currentDaySmsgArray) == 1:
                currentDaySmsg = currentDaySmsgArray[0]
                allServersCurrentDayMsg.append(currentDaySmsg)
            else:
                continue

            try:
                allDayServerInfoArr = getServerMsg(headers, loginSession, sId, '2017-06-15 00:00:00')  # 获取该服所有天数信息
                if allDayServerInfoArr:
                    allReg = 0
                    for s in allDayServerInfoArr:
                        allReg = allReg + int(s.newRole)
                    currentDaySmsg.allDayReg = allReg

                allDayPay = getPay(headers, loginSession,sId, '2017-06-15 00:00:00')
                currentDaySmsg.allDayPay = allDayPay

                currentDaySmsg.ltv = str(round(allDayPay/allReg,2))
            except:
                pass


        allServersCurrentDayMsg = getRetimeOnline(headers, loginSession,serverIds,allServersCurrentDayMsg)
        return allServersCurrentDayMsg

def getPay(headers, loginSession, serverIds,startTime):
    payUrl = 'http://jllrcsss-tw.starb168.com/gameManager/pay/sts.do'
    values = {
        'nowPage': '1',
        'serverId': serverIds,
        'gmpay': 1,
        'type': 1,
        'startTime': startTime,
        'endTime': get_current_time2(),
        'page': '1',
        'rows': '20'
    }
    s = loginSession.post(payUrl, data=values, headers=headers)
    payDatas = json.loads(s.text)
    rowsData = payDatas.get('rows')
    pays = 0
    if rowsData:
        for d in rowsData:
            pays = pays + d.get('count')
    return pays


def getRetimeOnline(headers, loginSession, serverIds, listSmsg):
    retimeUrl = 'http://jllrcsss-tw.starb168.com/gameManager/onlineST/inquire.do'
    values = {
        'nowPage': '1',
        'serverId': ','.join(serverIds),
        'page': '1',
        'rows': '20'
    }
    s = loginSession.post(retimeUrl, data=values,headers=headers)
    print s.text
    retimeDatas = json.loads(s.text)
    dataArray = retimeDatas.get('rows')
    if dataArray:
        for d in dataArray:
            sId = d.get('serverId')
            retimeOnlie_a = d.get('num')
            if not retimeOnlie_a:
                retimeOnlie_a = 0
            for sMsg in listSmsg:
                if sId == sMsg.serverName:
                    sMsg.ccu = retimeOnlie_a
    return listSmsg




def getServers(headers, loginSession):
    mUrl = 'http://jllrcsss-tw.starb168.com/gameManager/serverConfig/init.do'
    s = loginSession.post(mUrl, headers=headers)
    print s.text
    serverList = json.loads(s.text)
    if serverList:
        serverIds = []
        for obj in serverList:
            serverId = obj.get('serverId')
            if serverId == 1000:
                pass
            else:
                serverIds.append(str(serverId))
    return serverIds


def getServerMsg(headers, loginSession,serverId,startTime):
    showDailyReportDo = 'http://jllrcsss-tw.starb168.com/gameManager/pay/showDailyReport.do'
    # startTime = get_current_time() + ' 00:00:00'
    values = {
        'serverId': serverId,
        'startTime': startTime,
        'endTime': get_current_time2(),
        'gmpay': '1'
    }
    s = loginSession.post(showDailyReportDo, data=values, headers=headers)
    # print s.text
    try:
        parsed_json = json.loads(s.text)
    except:
        print 'parsed_json = json.loads(s.text) error'
        return None
    if parsed_json:
        serverArry = parsed_json.get('rows')
        if serverArry:
            sMsgArray = []
            for obj in serverArry:
                platform = obj.get('platform')
                # if platform == '全平台':
                if platform == 'Starpy':
                    newID = obj.get('newID')  # 新增账号
                    liveID = obj.get('liveID')  # 活跃账号
                    payUser = obj.get('payUser')  # 付费用户
                    payPercent = obj.get('payPercent')  # 付费率
                    liveARPU = obj.get('liveARPU')  # 活跃arpu
                    income = obj.get('income')  # 当日收入
                    newARPU = obj.get('newARPU')  # 新增arpu
                    payARPU = obj.get('payARPU')  # 付费arpu

                    sMsg = ServerMsg()
                    sMsg.gameName = u'精灵王国'
                    sMsg.newRole = newID
                    sMsg.newARPPU = newARPU
                    sMsg.arppu = payARPU
                    sMsg.totalPay = income
                    sMsg.totalRolePay = payUser
                    sMsg.payPercent = payPercent
                    sMsg.serverName = serverId
                    sMsg.roleLogin = liveID
                    sMsgArray.append(sMsg)

            return sMsgArray
    return None


if __name__ == '__main__':
    requestData()