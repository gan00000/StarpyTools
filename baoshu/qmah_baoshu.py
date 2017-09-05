#-*- coding: UTF-8 -*-
import simplejson as json
import re
import sys
import time
import types
from bs4 import BeautifulSoup
import chardet

from baoshu.smsgtool import sumSmsg
from excel.excelutil import writeExcelForGameInfo

reload(sys)
sys.setdefaultencoding('utf-8')

from baoshu import time_helper
from baoshu.ServerMsg import ServerMsg
from baoshu.AccountLogin import Login


def loginQmah():
    mLogin = Login()
    loginPage = 'http://sd.q5.com/index.php/login'
    loginPostUrl = 'http://sd.q5.com/index.php/admin/login/checklogin'
    postVaule = {
        'username': 'qiaozhi',
        'password': '999999'
    }
    headers = {
        'Referer': 'http://sd.q5.com/index.php/login',
        'Host': 'sd.q5.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    # menupage,urllib2 = userlogin.login(loginPostUrl,postVaule,headers,'hajj_cookies')
    login_success_page, login_session = mLogin.session_login(loginPage, loginPostUrl, postVaule, headers, 'qmah_cookies')
    mainPage = login_session.get('http://sd.q5.com/index.php/main', headers=headers)

    # print mainPage.text
    return headers, login_session

def getServerMap(login_headers,login_session):
    today = time_helper.get_current_time()
    url = 'http://sd.q5.com/index.php/functionlist/game_func/107?start=' + today + '&end=' + today + '&serverid=0'

    contentPage = login_session.get(url)
    # utf8string = unicode.encode(contentPage.text,"utf-8")
    # print utf8string
    # print(chardet.detect(contentPage.text))
    soup_s_data = BeautifulSoup(contentPage.content, 'html.parser')

    #  在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
    servers_info_array = soup_s_data.find_all('a', class_='s-m-astyle server_tan')
    if servers_info_array:
        servers_map = {}
        for server_info in servers_info_array:
            server_id = server_info['id']
            if server_id:
                server_id = server_id.replace('server_','')
                server_name = server_info.string
                print server_id + ':' + server_name
                servers_map[server_id] = server_name

        return servers_map
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


def getAllDataQmah():
    headers, login_session = loginQmah()
    servers_map = getServerMap(headers,login_session)

    sMsg_array = []
    for k,v in servers_map.items():
        if k == '0' or k == '999':
            continue
        sMsg = ServerMsg()
        sMsg.gameName = u'破战'
        sMsg.serverName = v
        try:
            getServer_ccu(login_session, sMsg, k)
        except:
            pass
        try:
            getServerPayData(login_session, sMsg, k)
        except:
            pass
        try:
           totalPay = getServerAllPay(login_session, sMsg, k)
           allReg = getServerAllReg(login_session, sMsg, k)
           if allReg:
               ltv = round(totalPay / allReg,2)
               sMsg.ltv = ltv
        except Exception, e:
            print 'error message:', e.message
            pass
        sMsg_array.append(sMsg)

    if len(sMsg_array) > 0:
        listSmsg = sumSmsg(sMsg_array)
        writeExcelForGameInfo('E:\\jingling\\qmah_baoshu.xls', u'破战 %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))), listSmsg)


def getServer_ccu(login_session,sMsg ,serverId):
    mValues = {
        'serverid':serverId
    }
    result = login_session.post('http://sd.q5.com/index.php/main/sel_server', data=mValues)
    result_info = login_session.get('http://sd.q5.com/index.php/functionlist/game_func/105')
    # print result_info.content
    ccu_html_data = BeautifulSoup(result_info.content, 'html.parser')
    # print ccu_html_data.script
    script_strings = ccu_html_data.find_all('script', text=re.compile(u"当日在线"))
    for script in script_strings:
        # if script.content:
        ccu_info = script.text.strip()
        ccu_info_array = ccu_info.split('\n')
        for line in ccu_info_array:
            line_q = line.strip()
            if 'data: [' in line_q:
                line_q_m = line_q.replace('[', '').replace('],', '')
                print line_q_m
                ccu_s_array = line_q_m.split(',')
                ccu = ccu_s_array[-1]

                print 'ccu:' + ccu
                sMsg.ccu = int(ccu)
                break


if __name__ == '__main__':

    a = 'kdakkglk236'
    print a[-2:-1]
    getAllDataQmah()