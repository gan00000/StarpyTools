#-*- coding: UTF-8 -*-
import time

from bs4 import BeautifulSoup

from baoshu.AccountLogin import Login
from baoshu.bmdzz_info import bmdzzinfo
from baoshu.time_helper import current_timestamp

import sys
#解决 UnicodeDecodeError: 'ascii' codec can't decode 报错
reload(sys)
sys.setdefaultencoding('utf8')

def getNewServerData(login_session):

    timestamp = current_timestamp()
    new_server_url = 'http://bamei.gemjy.cn:8089/index.php/server/new?_=' + str(timestamp)
    headers = {
        'Referer': 'http://bamei.gemjy.cn:8089/index.php/default/index',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    new_server_rep = login_session.get(new_server_url,headers = headers)
    if new_server_rep:

        new_server_result = new_server_rep.text
        print new_server_result
        soup = BeautifulSoup(new_server_result, 'html.parser')
        server_first = soup.tbody.tr
        parseServerInfo(server_first)

        for sibling in server_first.next_siblings:
            parseServerInfo(sibling)

            # server_ip_list = soup.find_all(name='option',value=re.compile('http://'))
    else:
        print 'error'


def parseServerInfo(server):
    if server:
        if server == '\n':
            print "sibling error"

        else:
            # print sibling
            td_list = server.find_all('td')
            if td_list:
                bmdzzinfo_a = bmdzzinfo()
                bmdzzinfo_a.data = td_list[0].string
                bmdzzinfo_a.serverName = td_list[1].string
                bmdzzinfo_a.newRole = td_list[2].string
                bmdzzinfo_a.roleLogin = td_list[3].string
                bmdzzinfo_a.newPayRole = td_list[4].string
                bmdzzinfo_a.newPay = td_list[5].string
                bmdzzinfo_a.newPayRate = td_list[6].string
                bmdzzinfo_a.newARPPU = td_list[7].string
                bmdzzinfo_a.totalRolePay = td_list[8].string
                bmdzzinfo_a.totalPay = td_list[9].string
                bmdzzinfo_a.arppu = td_list[10].string
                all_info.append(bmdzzinfo_a)
                # for td_tag in td_list:
                #     print td_tag.string


def bmdzzbaoshu():
    global all_info
    all_info = []
    mLogin = Login()
    loginPage = 'http://bamei.gemjy.cn:8089/index.php/default/login'
    loginPostUrl = 'http://bamei.gemjy.cn:8089/index.php/default/login'
    postVaule = {
        'User': 'qianlei',
        'Pass': 'Qianlei1234'
    }
    headers = {
        'Referer': 'http://bamei.gemjy.cn:8089/index.php/default/login',
        'Cookie': 'PHPSESSID = ffds8b7useid2eq6n3jqsvvt10',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    login_success_page, login_session = mLogin.session_login(loginPage, loginPostUrl, postVaule, headers,
                                                             'bmdzz_cookies')
    # print login_success_page.text
    getNewServerData(login_session)
    # print all_info
    # title = '日期     ' + '区服     ' + '新增角色数   ' + '角色登录数   ' + '新增付费角色数    ' + '新增收入   ' + '新增付费比    ' + '新增ARPPU    ' + '全部付费角色数   ' + '全部收入   ' + 'ARPPU\n'
    for s in all_info:
        if s.serverName is None or s.serverName.strip() == '狂人传说':
            pass
        else:
            baoshu_info = '区服:%s  新增角色数:%s  角色登录数:%s  新增付费角色数:%s  新增收入:%s  新增付费比:%s  新增ARPPU:%s  全部付费角色数:%s  全部收入:%s  ARPPU:%s' % (
            s.serverName, s.newRole, s.roleLogin, s.newPayRole, s.newPay, s.newPayRate, s.newARPPU, s.totalRolePay,
            s.totalPay, s.arppu)
            print baoshu_info

    return baoshu_info


if __name__ == '__main__':

    bmdzzbaoshu()