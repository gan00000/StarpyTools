#-*- coding: UTF-8 -*-
import time

from bs4 import BeautifulSoup

from baoshu.AccountLogin import Login
from baoshu.bmdzz_info import bmdzzinfo
from baoshu.time_helper import current_timestamp, get_current_time

import sys
from excel.excelutil import *
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

    new_server_rep = login_session.get(new_server_url,headers=headers)
    if new_server_rep:

        new_server_result = new_server_rep.text
        # print new_server_result
        soup = BeautifulSoup(new_server_result, 'html.parser')
        server_first = soup.tbody.tr
        bmdzzinfo_first = parseServerInfo(server_first)
        all_info = []
        all_info.append(bmdzzinfo_first)
        for sibling in server_first.next_siblings:
            bmdzzinfo_sibling = parseServerInfo(sibling)
            if bmdzzinfo_sibling:
                all_info.append(bmdzzinfo_sibling)

        return all_info

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
                # all_info.append(bmdzzinfo_a)
                # for td_tag in td_list:
                #     print td_tag.string
                return bmdzzinfo_a


def getServerInfoFromData(login_session, startDay, endDay):

    new_server_url = 'http://bamei.gemjy.cn:8089/index.php/server/new'

    headers = {
        'Referer': 'http://bamei.gemjy.cn:8089/index.php/default/index',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    postNewVaule = {
        'act': 'search',
        'startDay': startDay,
        'endDay': endDay
    }

    new_server_rep = login_session.post(new_server_url, data=postNewVaule, headers=headers)
    if new_server_rep:

        new_server_result = new_server_rep.text
        # print new_server_result
        soup = BeautifulSoup(new_server_result, 'html.parser')
        server_first = soup.tbody.tr
        all_server_info = []
        bmdzzinfo_first = parseServerInfo(server_first)
        all_server_info.append(bmdzzinfo_first)
        for sibling in server_first.next_siblings:
            bmdzzinfo_sibling = parseServerInfo(sibling)
            if bmdzzinfo_sibling:
                all_server_info.append(bmdzzinfo_sibling)
        return all_server_info

    else:
        print 'error'


def bmdzzbaoshu():

    all_server_info = []
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
    all_info = getNewServerData(login_session)
    # print all_info
    # title = '日期     ' + '区服     ' + '新增角色数   ' + '角色登录数   ' + '新增付费角色数    ' + '新增收入   ' + '新增付费比    ' + '新增ARPPU    ' + '全部付费角色数   ' + '全部收入   ' + 'ARPPU\n'
    # for s in all_info:
    #     if s.serverName is None or s.serverName.strip() == '狂人传说':
    #         pass
    #     else:
    #         baoshu_info = '区服:%s  新增角色数:%s  角色登录数:%s  新增付费角色数:%s  新增收入:%s  新增付费比:%s  新增ARPPU:%s  全部付费角色数:%s  全部收入:%s  ARPPU:%s' % (
    #             s.serverName, s.newRole, s.roleLogin, s.newPayRole, s.newPay, s.newPayRate, s.newARPPU, s.totalRolePay,
    #             s.totalPay, s.arppu)
    #
    # baoshu_info = '把妹大作战数据:\n' + baoshu_info
    # print baoshu_info
    #
    # #ltv
    # all_server_info = getServerInfoFromData(login_session, '2017-05-18', get_current_time())
    # if len(all_server_info) > 0:
    #     ltv = 'LTV如下:\n'
    #     for ss in all_server_info:
    #         if ss.serverName is None or ss.serverName.strip() == '狂人传说':
    #             pass
    #         else:
    #             if ss.totalPay and ss.newRole:
    #
    #                 ltv = ltv + '区服:%s LTV: %s' % (ss.serverName, str(round(float(ss.totalPay) / float(ss.newRole),2))) + '\n'
    #
    # print ltv
    # baoshu_info = baoshu_info + '\n\n' + ltv
    # print baoshu_info
    createXls(login_session,all_info)
    return ''

def createXls(login_session, all_info):
    #ltv
    all_server_info = getServerInfoFromData(login_session, '2017-05-18', get_current_time())
    if len(all_server_info) > 0:
        for ss in all_server_info:
            if ss.serverName is None or ss.serverName.strip() == '狂人传说':
                pass
            else:
                if ss.totalPay and ss.newRole:
                    print 'totalPay:' + ss.totalPay + '---newRole:' + ss.newRole
                    ss.ltv = str(round(float(ss.totalPay) / float(ss.newRole), 2))
                    # ltv = ltv + '区服:%s LTV: %s' % (ss.serverName, str(round(float(ss.totalPay) / float(ss.newRole),2))) + '\n'


    title = [u'区服',u'新增角色数',u'角色登录数',u'新增付费角色数',u'新增收入',u'新增付费比',u'新增ARPPU',u'全部付费角色数',u'全部收入',u'ARPPU',u'LTV']
    excel = xlwt.Workbook()  # 创建工作簿
    sheet1 = excel.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    role_game_title = [u'把妹大作战 %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))]
    sheet1.write_merge(0, 0, 0, 10)
    write_row = 0
    sheet1.write(write_row, 0, role_game_title, set_style('Times New Roman', 220, True))
    write_row = write_row + 1

    for i in range(0, len(title)):
        sheet1.write(write_row, i, title[i], set_style('Times New Roman', 220, True))
    write_row = write_row + 1
    style = create_wrap_centre()

    for s in all_info:
        if s.serverName is None or s.serverName.strip() == '狂人传说':
            pass
        else:
            content = [s.serverName, s.newRole, s.roleLogin, s.newPayRole, s.newPay, s.newPayRate, s.newARPPU, s.totalRolePay, s.totalPay, s.arppu]

            for ss in all_server_info:#拼接ltv
                if ss.serverName == s.serverName:
                    content.append(ss.ltv)

            for i in range(0, len(content)):
                sheet1.write(write_row, i, content[i], style)
            write_row = write_row + 1
    excel.save('E:\\jingling\\bmdzz_baoshu.xls')  # 保存文件

if __name__ == '__main__':

    bmdzzbaoshu()

