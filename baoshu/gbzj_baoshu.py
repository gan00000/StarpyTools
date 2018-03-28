#-*- coding: UTF-8 -*-
import simplejson as json
import re
import sys
import time
import types
from bs4 import BeautifulSoup

from baoshu.smsgtool import sumSmsg
from excel.excelutil import writeExcelForGameInfo, writeExcelForGameInfo_new

reload(sys)
sys.setdefaultencoding('utf-8')

from baoshu import time_helper
from baoshu.ServerMsg import ServerMsg
from baoshu.AccountLogin import Login


def loginTWZJ():
    mLogin = Login()
    loginPage = 'http://sso.kaixin002.com'
    loginPostUrl = 'http://sso.kaixin002.com/?mod=accounts&act=login'
    postVaule = {
        'user_name': 'twxingbi',
        'user_password': 'tw1234XBi',
        'submit.x': '55',
        'submit.y': '21'
    }
    headers = {
        'Referer': 'http://sso.kaixin002.com/?mod=accounts&act=login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'sso.kaixin002.com',
    }
    # menupage,urllib2 = userlogin.login(loginPostUrl,postVaule,headers,'hajj_cookies')
    login_success_page, login_session = mLogin.session_login(loginPage, loginPostUrl, postVaule, headers, 'gbzj_cookies')

    main_page = login_session.get('http://sso.kaixin002.com/')
    # print main_page.text

    return headers, login_session
#http://sso2.kaixin002.com/fd/index.php?act=kx.total&aid=5672&lk=%B8%D6%CC%FA%D5%BD%D5%F9_%D7%DC%CC%E5%CA%FD%BE%DD&treeid=5672000
def getServerList(login_headers,login_session):
    s_url = 'http://sso2.kaixin002.com/fd/index.php?act=kx.total&aid=5682&lk=General+Kim_%D7%DC%CC%E5%CA%FD%BE%DD&treeid=5682000'

    contentPage = login_session.get(s_url)

    soup_s_data = BeautifulSoup(contentPage.text, 'html.parser')

    servers_list = []

    serverList = soup_s_data.find_all('select')
    if serverList and serverList[0]:
        server_option_list = serverList[0].find_all('option')

        if server_option_list:  # 遍列服务器 id 和 名称
            for server_option in server_option_list:

                s_value = server_option['value']
                s_string = server_option.string
                if u'全服汇总' == s_string:
                    continue

                if u'972' == s_value:
                    continue

                if u'973' == s_value:
                    continue
                print s_value
                print s_string
                serverMsg = ServerMsg()
                serverMsg.serverId = s_value
                serverMsg.serverName = s_string
                servers_list.append(serverMsg)

    return servers_list

def getServerInfo(login_headers,login_session, sMsg):

    today = time_helper.get_current_time()
    # http: // mthxtw.gm.starpytw.com / Stat / realTime
    s_info_url = 'http://sso2.kaixin002.com/fd/index.php?sdate=' + today + '&edate=' + today + '&sid=' + sMsg.serverId \
                 + '&act=kx.total&treeid=5682000&day=&day2=day&aid=5682&lk=General+Kim_%D7%DC%CC%E5%CA%FD%BE%DD&Submit=%B2%E9%D1%AF'

    contentPage = login_session.get(s_info_url , headers=login_headers)
    # print contentPage.text

    soup_s_data = BeautifulSoup(contentPage.text, 'html.parser')


    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    s_infos = soup_s_data.find_all('tr')

    s_info_tr = s_infos[len(s_infos) -1]
    tdlist = s_info_tr.find_all('td')
    if tdlist:

        newRole = tdlist[9].string
        if newRole:
            sMsg.newRole = newRole
        else:
            sMsg.newRole = 0
        dau = tdlist[6].string
        if dau:
            sMsg.roleLogin = dau
        else:
            sMsg.roleLogin = 0
        sMsg.allDayReg = 0

        sMsg.totalPay = 0
        totalPay = tdlist[15].string
        if totalPay:
            sMsg.totalPay = totalPay

        if sMsg.totalPay > 0:
            sMsg.totalPay =float(sMsg.totalPay)
            # sMsg.totalPay = round(float(sMsg.totalPay) / 8, 2)

        newPayRole = tdlist[18].string
        if newPayRole:
            sMsg.newPayRole = int(newPayRole)
        else:
            sMsg.newPayRole = 0

        sMsg.totalRolePay = 0
        totalRolePay = tdlist[19].string
        if totalRolePay:
            sMsg.totalRolePay = int(totalRolePay)
        else:
            sMsg.totalRolePay = 0
        if sMsg.totalRolePay > 0:
            sMsg.arppu = round(sMsg.totalPay / sMsg.totalRolePay, 2)

        sMsg.payPercent = tdlist[20].string
        sMsg.gameName = u'General Kim'

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
        if int( sMsg.allDayReg) > 0:
            sMsg.ltv = round(sMsg.allDayPay / sMsg.allDayReg, 2)
        print sMsg.allDayPay


def getServerCCU(login_headers,login_session, sMsg):
    today = time_helper.get_current_time()
    url = 'http://sso2.kaixin002.com/fd/index.php?sdate=' + today + '&edate=' + today + '&sid=' + sMsg.serverId + '&act=kx.serveronline&treeid=5682001&day=fiveminute&aid=5682&lk=General+Kim_%D4%DA%CF%DF%CA%FD%BE%DD'
    data = login_session.get(url, headers=login_headers)

    ccu_s_data = BeautifulSoup(data.text, 'html.parser')
    table_ccu = ccu_s_data.find_all(id="newtb")
    tr_list = table_ccu[0].find_all('tr')
    if tr_list:
        td_list = tr_list[1].find_all('td')
        if td_list:
            ccu = td_list[2].string
            print(sMsg.serverId + ' ccu is ' + ccu)
            sMsg.ccu = int(ccu)

def getAllDataGBZJ():
    headers, login_session = loginTWZJ()

    sMsg_array = getServerList(headers, login_session)
    for sMsg in sMsg_array:
        s = getServerInfo(headers, login_session, sMsg)
        s = getServerCCU(headers, login_session, sMsg)
        # getServerAllPay(headers, login_session, sMsg)


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
        writeExcelForGameInfo_new('E:\\jingling\\gbzj_baoshu.xls', u'General Kim %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))), listSmsg)

if __name__ == '__main__':
    getAllDataGBZJ()