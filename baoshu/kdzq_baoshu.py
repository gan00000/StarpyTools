#-*- coding: UTF-8 -*-
import requests
import simplejson as json
import re
import sys
import time
import types
from bs4 import BeautifulSoup

from baoshu.smsgtool import sumSmsg
from baoshu.time_helper import current_timestamp
from excel.excelutil import writeExcelForGameInfo, writeExcelForGameInfo_new

reload(sys)
sys.setdefaultencoding('utf-8')

from baoshu import time_helper
from baoshu.ServerMsg import ServerMsg
from baoshu.AccountLogin import Login
from urllib import quote

def loginTWZJ():
    mLogin = Login()
    loginPage = 'http://gm-kdzqen.starpyse.com/manage/index.php?c=main&a=login'
    loginPostUrl = 'http://gm-kdzqen.starpyse.com/manage/index.php?c=main&a=login_post'
    postVaule = {
        'username': 'starpy',
        'password': '123456',
        'refer': 'index'
    }
    headers = {
        'Referer': 'http://gm-kdzqen.starpyse.com/manage/index.php?c=main&a=login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'gm-kdzqen.starpyse.com',
    }
    # menupage,urllib2 = userlogin.login(loginPostUrl,postVaule,headers,'hajj_cookies')
    login_success_page, login_session = mLogin.session_login(loginPage, loginPostUrl, postVaule, headers, 'kdzq_cookies')

    # main_page = login_session.get('http://sso.kaixin002.com/')
    # print login_success_page.text

    return headers, login_session,login_success_page
#http://sso2.kaixin002.com/fd/index.php?act=kx.total&aid=5672&lk=%B8%D6%CC%FA%D5%BD%D5%F9_%D7%DC%CC%E5%CA%FD%BE%DD&treeid=5672000

def getServerList(login_headers,login_session,login_success_page):

    soup_s_data = BeautifulSoup(login_success_page.text, 'html.parser')

    servers_list = []

    serverList = soup_s_data.find_all('select')
    if serverList and serverList[0]:
        server_option_list = serverList[0].find_all('option')

        if server_option_list:  # 遍列服务器 id 和 名称
            for server_option in server_option_list:

                s_value = server_option['host']
                s_string = server_option.string
                print s_value + "   " + s_string

                serverMsg = ServerMsg()
                serverMsg.serverId = s_value
                serverMsg.serverName = s_string
                servers_list.append(serverMsg)

    return servers_list

def getServerInfo(login_headers,login_session, sMsg):


    s_url = "http://gm-kdzqen.starpyse.com/manage/index.php?c=main&a=change&group=%s&host=%s" % (quote(sMsg.serverName),sMsg.serverId)
    print s_url
    s_page = login_session.get(s_url,headers=login_headers,cookies = login_session.cookies)

    today = time_helper.get_current_time()
    # http: // mthxtw.gm.starpytw.com / Stat / realTime

    # 'http://gm-kdzqen.starpyse.com/manage/index.php?c=stat_report&a=online&start_time=2018-06-15&stop_time=2018-06-15'
    s_cc_url = 'http://gm-kdzqen.starpyse.com/manage/index.php?c=stat_report&a=online&start_time =' + today + '&stop_time=' + today


    contentPage = login_session.get(s_cc_url , headers=login_headers,cookies = login_session.cookies)
    # print contentPage.text

    soup_s_data = BeautifulSoup(contentPage.text, 'html.parser')


    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    # s_infos = soup_s_data.find_all('tr')
    #
    # s_info_tr = s_infos[len(s_infos) -1]
    # tdlist = s_info_tr.find_all('td')
    # if tdlist:
    #
    #
    #     newRole = tdlist[9].string
    #     if newRole:
    #         sMsg.newRole = newRole
    #     else:
    #         sMsg.newRole = 0
    #     dau = tdlist[6].string
    #     if dau:
    #         sMsg.roleLogin = dau
    #     else:
    #         sMsg.roleLogin = 0
    #     sMsg.allDayReg = 0
    #
    #     sMsg.totalPay = 0
    #     totalPay = tdlist[16].string
    #     if totalPay:
    #         sMsg.totalPay = totalPay
    #
    #     if sMsg.totalPay > 0:
    #         # sMsg.totalPay =float(sMsg.totalPay)
    #         sMsg.totalPay = round(float(sMsg.totalPay) / 8, 2)
    #
    #     newPayRole = tdlist[18].string
    #     if newPayRole:
    #         sMsg.newPayRole = int(newPayRole)
    #     else:
    #         sMsg.newPayRole = 0
    #
    #     sMsg.totalRolePay = 0
    #     totalRolePay = tdlist[19].string
    #     if totalRolePay:
    #         sMsg.totalRolePay = int(totalRolePay)
    #     else:
    #         sMsg.totalRolePay = 0
    #     if sMsg.totalRolePay > 0:
    #         sMsg.arppu = round(sMsg.totalPay / sMsg.totalRolePay, 2)
    #
    #     sMsg.payPercent = tdlist[20].string
    #
    #
    #     sMsg.gameName = u'決戰金將軍'

        # return sMsg


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
    # 'http://gm-kdzqen.starpyse.com/manage/index.php?c=main&a=change&group=%E8%8B%B1%E6%96%87:%E6%AD%A3%E5%BC%8F%E6%9C%8D&host=240002'
    sName = '%E8%8B%B1%E6%96%87:%E6%AD%A3%E5%BC%8F%E6%9C%8D' #quote(sMsg.serverName.encode('UTF-8'))

    s_url = "http://gm-kdzqen.starpyse.com/manage/index.php?c=main&a=change&group=%s&host=%s" % (sName, sMsg.serverId)
    print s_url
    s_page = login_session.get(s_url, headers=login_headers,cookies = login_session.cookies)

    login_session.get('http://gm-kdzqen.starpyse.com/manage/index.php?c=main&a=home',cookies = login_session.cookies)

    today = time_helper.get_current_time()
    # http: // mthxtw.gm.starpytw.com / Stat / realTime

    # 'http://gm-kdzqen.starpyse.com/manage/index.php?c=stat_report&a=online&start_time=2018-06-15&stop_time=2018-06-15'
    # s_cc_url = 'http://gm-kdzqen.starpyse.com/manage/index.php?c=stat_report&a=online&start_time =' + today + '&stop_time=' + today
    s_cc_url = 'http://gm-kdzqen.starpyse.com/manage/index.php?c=stat_report&a=online'

    contentPage = login_session.get(s_cc_url, headers=login_headers,cookies = login_session.cookies)
    # print contentPage.text

    ccu_s_data = BeautifulSoup(contentPage.text, 'html.parser')
    # table_ccu = ccu_s_data.find_all(_class="body")
    # if table_ccu and table_ccu[0]:
    td_list = ccu_s_data.find_all('td')
    if td_list:
        td = td_list[len(td_list) - 1]
        if td:
            span_list = td.find_all('span')
            if span_list:
                ccu= span_list[0].string
                print(sMsg.serverId + ' ccu is ' + ccu)
                sMsg.ccu = int(ccu)
            else:
                ccu = td.string
                sMsg.ccu = int(ccu)
                print(sMsg.serverId + ' ccu is ' + ccu)


def getAllDataKdzq():
    headers, login_session,login_success_page = loginTWZJ()

    sMsg_array = getServerList(headers, login_session,login_success_page)
    for sMsg in sMsg_array:
        s = getServerCCU(headers, login_session, sMsg)

    url = 'http://manager.starpyse.com/fn/data/statistics?gameCode=kdzq&aa=' + str(current_timestamp())
    res = requests.get(url)
    print res.text
    if res:
        res_json = json.loads(res.text)
        array_s = res_json.get('topup')
        register = res_json.get('register')
        print(register)
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

                for s_a in sMsg_array:
                    if serverName in s_a.serverName:
                        sm.serverName = s_a.serverName
                        sm.ccu = s_a.ccu
                        break


                s_info_list.append(sm)

            listSmsg = sumSmsg(s_info_list)

            writeExcelForGameInfo('/Users/gan/qyst/testasaa.xls',
                                  u'口袋足球 %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))),
                                  listSmsg)


if __name__ == '__main__':
    getAllDataKdzq()

