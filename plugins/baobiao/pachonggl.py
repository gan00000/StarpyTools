#-*- coding: UTF-8 -*-
import sys
import types

reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import urllib
import cookielib
import os
import re
import requests
from AllConfig import *
from Serverinfo import *
import time
import simplejson as json
from online_config import *
import datetime
import collections
from excel.excelutil import *

def product_cookies(msession):
    cookies_str = ''
    for item in msession.cookies:
        print item.name + ':' + item.value
        cookies_str = cookies_str + item.name + ':' + item.value + ';'
    cookies_str = cookies_str[:-1]
    print 'cookies_str-->' + cookies_str
    return cookies_str


def get_current_time():
    # print time.time()
    t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print 'time:' + t
    return t

def get_moth_before_time():
    mothAgo = (datetime.datetime.now() - datetime.timedelta(days=26))
    t = mothAgo.strftime('%Y-%m-%d')
    print '30 day time:' + t
    return t


def getServerInfo(session, serverId):
    # 选服
    server_response = session.get("http://210.68.122.121/master/duoluotaitanGM/?area_selected_id=" + serverId)
    # print server_response.text
    # 根据角色
    data_role_url = "http://210.68.122.121/master/duoluotaitanGM/businessdata/businessmanagerrole"
    session.get(data_role_url)

    serverinfo = getCurrentDaySinfo(data_role_url, serverId, session)

    if int(serverId) > 0:
        getMothDaySinfo(serverinfo,data_role_url,session)

    print "sever_id:" + serverinfo.sever_id + "  register_roles:" + serverinfo.register_roles + " login_roles:" + serverinfo.login_roles
    return serverinfo


def getMothDaySinfo(serverinfo,data_role_url, session):
    # 选择日期
    data_role_url_params = {'row[starttime]': get_moth_before_time()}
    data_role_url_header = {'Referer': 'http://210.68.122.121/master/duoluotaitanGM/businessdata/businessmanagerrole',
                            'Origin': 'http://210.68.122.121',
                            'Upgrade-Insecure-Requests': '1'}
    data_role_url_response = session.post(data_role_url, data=data_role_url_params, headers=data_role_url_header).text
    # print data_role_url_response.text
    register_role_re = re.compile(r'<td>&nbsp; \w+</td>')
    # register_role_re = re.compile(r'<td>注册角色</td>\w+<td>角色登录总数</td>')
    # register_role_re = re.compile("<td>注册角色</td>[\w]{*}</tr>")
    # data_role_url_response_1 = data_role_url_response.text.replace('\r\n','').replace(' ','')
    data_role_url_response_temp = data_role_url_response[
                                  data_role_url_response.index('<td>注册角色</td>'):data_role_url_response.index(
                                      '<td>角色登录总数</td>')]
    # serverinfo = Serverinfo()
    # serverinfo.sever_id = serverId
    temt_list = register_role_re.findall(data_role_url_response_temp)
    suzi_list_re = re.compile(r'\d+')#得到所有注册记录
    for register_item in temt_list:
        suzi_list = suzi_list_re.findall(register_item)
        item_count  = suzi_list[0]
        serverinfo.allRegister = serverinfo.allRegister + int(item_count)
    return serverinfo

def getCurrentDaySinfo(data_role_url, serverId, session):
    # 选择日期
    data_role_url_params = {'row[starttime]': get_current_time()}
    data_role_url_header = {'Referer': 'http://210.68.122.121/master/duoluotaitanGM/businessdata/businessmanagerrole',
                            'Origin': 'http://210.68.122.121',
                            'Upgrade-Insecure-Requests': '1'}
    data_role_url_response = session.post(data_role_url, data=data_role_url_params, headers=data_role_url_header).text
    # print data_role_url_response.text
    register_role_re = re.compile(r'<td>&nbsp; \w+</td>')
    # register_role_re = re.compile(r'<td>注册角色</td>\w+<td>角色登录总数</td>')
    # register_role_re = re.compile("<td>注册角色</td>[\w]{*}</tr>")
    # data_role_url_response_1 = data_role_url_response.text.replace('\r\n','').replace(' ','')
    data_role_url_response_temp = data_role_url_response[
                                  data_role_url_response.index('<td>注册角色</td>'):data_role_url_response.index(
                                      '<td>角色登录总数</td>')]
    serverinfo = Serverinfo()
    serverinfo.sever_id = serverId
    temt_list = register_role_re.findall(data_role_url_response_temp)
    suzi_list_re = re.compile(r'\d+')
    suzi_list = suzi_list_re.findall(temt_list[0])
    serverinfo.register_roles = suzi_list[0]
    data_role_url_response_temp = data_role_url_response[
                                  data_role_url_response.index('<td>角色登录总数</td>'):data_role_url_response.index(
                                      '<td>留存的开服当天角色数</td>')]
    temt_list = register_role_re.findall(data_role_url_response_temp)
    suzi_list = suzi_list_re.findall(temt_list[0])
    serverinfo.login_roles = suzi_list[0]

    return serverinfo


def realtime(session,all_config):
    realtime_header = {'Referer':'http://210.68.122.121/master/duoluotaitanGM/index'}
    session.get("http://210.68.122.121/master/duoluotaitanGM/area/realtime",headers=realtime_header)

    realtime_params = {
        "page": "1",
        "rp": "50",
        "sortname":'',
            "sortorder":'',
    'query':'',
    'qtype':"",
    'qop':'=',
    'colkey':'id',
    'colsinfo':'id, name, currentonline, maxonline, registercount, updatetime, state',
    'aliasinfo':'id, name, currentonline, maxonline, registercount, updatetime, state'
    }

    realtime_result = session.post("http://210.68.122.121/master/duoluotaitanGM/area/realtime/flexigrid?_=1493106566716",data= realtime_params)
    # print realtime_result.text

    parsed_json = json.loads(realtime_result.text)
    json_array = parsed_json.get("rows")
    onlinecfg_list = []
    for obj in json_array:
        # print obj.get('id')
        json_cell = obj.get('cell')
        if json_cell is not None:
            onlinecfg = online_config()
            onlinecfg.server_id = str(json_cell.get('id'))
            currentOnLine = json_cell.get('currentonline');
            aa = "<label style='color:#999999'>"
            if type(currentOnLine) is types.IntType:
                entonline = str(currentOnLine)

            else:
                if aa in currentOnLine:
                    onlineTemp = currentOnLine.replace(aa, '').replace("</label>", '')
                    entonline = onlineTemp
                else:
                    entonline = currentOnLine

            onlinecfg.currentonline = entonline
            onlinecfg_list.append(onlinecfg)
            set_all_config_online(all_config,onlinecfg)
            print onlinecfg.server_id + " 实时在线:" + onlinecfg.currentonline

    return onlinecfg_list


def set_all_config_online(all_config,onlinecfg):
    for f in all_config.server_info_list:
        if f.sever_id == onlinecfg.server_id:
            f.current_online = onlinecfg.currentonline
            return


# http://210.68.122.121/master/duoluotaitanGM/dbvip/payment/flexigrid?_=1493109987546
# page:1
# rp:20
# sortname:create_time
# sortorder:desc
# query:2017-04-25
# qtype:create_time
# qop:like
# colkey:platform
# colsinfo:roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id
# aliasinfo:roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id
# Name
# flexigrid?_=1493111107475

def payment(session,all_config):
    print '充值订单详情'
    _header = {'Referer': 'http://210.68.122.121/master/duoluotaitanGM/index'}
    session.get("http://210.68.122.121/master/duoluotaitanGM/dbvip/payment",headers=_header)
    payment_params = {
    "page": "1",
    "rp": '5000',
    'sortname':'create_time',
    'sortorder':'desc',
    'query':get_current_time(),
    'qtype':'create_time',
    'qop':'like',
    'colkey':'platform',
    'colsinfo': 'roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id',
    'aliasinfo':'roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id'

    }

    # 'colsinfo': 'roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id',
    # 'aliasinfo':'roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id'

    payment_result = session.post("http://210.68.122.121/master/duoluotaitanGM/dbvip/payment/flexigrid?_=1493111107475",data=payment_params,headers=_header)
    print payment_result.text
    parsed_json = json.loads(payment_result.text)
    if parsed_json is not None:
        json_array = parsed_json.get("rows")
        # all_config.pay_persions = len(json_array)
        if json_array:
            for obj in json_array:
                # print obj.get('id')
                json_cell = obj.get('cell')
                if json_cell is not None:
                   serverid = json_cell.get('serverid')
                   sum_pay(all_config, json_cell, str(serverid))


def payment_ltv(session,all_config,serverid):
    print 'ltv : ' + serverid
    _header = {'Referer': 'http://210.68.122.121/master/duoluotaitanGM/dbvip/payment'}
    session.get("http://210.68.122.121/master/duoluotaitanGM/dbvip/payment",headers=_header)

    # page:1
    # rp:10000
    # sortname:create_time
    # sortorder:desc
    # query:10
    # qtype:serverid
    # qop:=
    # colkey:platform
    # colsinfo:roleid, accountid, platform, channel, serverid, orderid, thirdorderid, money, create_time, finish_time, send_time, product_id, status, sending_time, id
    # aliasinfo:roleid, accountid, platform, channel, serverid, orderid, thirdorderid, money, create_time, finish_time, send_time, product_id, status, sending_time, id

    payment_params = {
    "page": "1",
    "rp": '10000',
    'sortname':'create_time',
    'sortorder':'desc',
    'query':serverid,
    'qtype':'serverid',
    'qop':'=',
    'colkey':'platform',
    'colsinfo': 'roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id',
    'aliasinfo':'roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id'
    }

    # 'colsinfo': 'roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id',
    # 'aliasinfo':'roleid,accountid,platform,channel,serverid,orderid,thirdorderid,money,create_time,finish_time,send_time,product_id,status,sending_time,id'

    payment_result = session.post("http://210.68.122.121/master/duoluotaitanGM/dbvip/payment/flexigrid?_=1493264982973",data=payment_params,headers=_header)
    # print "payment_result_ltv:" + payment_result.text
    parsed_json = json.loads(payment_result.text)
    if parsed_json is not None:
        json_array = parsed_json.get("rows")
        # all_config.pay_persions = len(json_array)
        if json_array is not None:
            for f in all_config.server_info_list:
                if f.sever_id == serverid:
                    for obj in json_array:
                        # print obj.get('id')
                        json_cell = obj.get('cell')
                        if json_cell is not None:
                           # serverid = json_cell.get('serverid')
                           sum_pay_ltv(f, json_cell, str(serverid))

def sum_pay_ltv(s_info, json_cell, serverid):
    money = json_cell.get('money')
    s_info.ltv_pay = s_info.ltv_pay + money


def sum_pay(all_config, json_cell, serverid):
    for f in all_config.server_info_list:
        if f.sever_id == serverid:
            money = json_cell.get('money')
            f.pays = f.pays + money
            return


def getAllPay(session,all_config_temp):
    print '玩家充值数据'
    url = 'http://210.68.122.121/master/duoluotaitanGM/businessdata/businesschargedata'
    all_res = session.get(url).text
    # print all_res

    all_res_temp = all_res[all_res.index('<td>当日流水</td>'):all_res.index('<!-- <canvas id="cvs" width="1700" height="500" style="border:')]

    shuzi = re.compile("[\d.%]+")
    shuzi_g = shuzi.findall(all_res_temp)

    for s in shuzi_g:
        print s
    all_config_temp.all_pay = shuzi_g[0]
    # all_config_temp.guanfang_pay = shuzi_g[1]
    # all_config_temp.others_pay = shuzi_g[2]
    all_config_temp.pay_persions = shuzi_g[1]
    all_config_temp.active_pay_rate = shuzi_g[2]
    all_config_temp.new_pay_rate=shuzi_g[3]
    all_config_temp.pay_arpu = shuzi_g[5]


def sendActivityWuPin(activity_list):
    from bs4 import BeautifulSoup
    url='http://210.68.122.121/master/duoluotaitanGM/mail/singlemail'
    send_header = {'Referer': 'http://210.68.122.121/master/duoluotaitanGM/'}
    login_page, m_seeion = session_login()
    sendres = m_seeion.get(url,headers=send_header)

    add_page_header = {'Referer': 'http://210.68.122.121/master/duoluotaitanGM/mail/singlemail'}
    add_page = m_seeion.get('http://210.68.122.121/master/duoluotaitanGM/mail/singlemail/add', headers=add_page_header)
    sendres_str = add_page.text
    print sendres_str

    soup = BeautifulSoup(sendres_str,'html.parser')

    server_ip_list = soup.find_all(name='option',value=re.compile('http://'))
    print server_ip_list
    server_ip = {}
    for ipitem in server_ip_list:
        string_text = ipitem.string
        ip = ipitem.get('value')
        print string_text
        string_text = string_text[0:2].replace('-','')
        print string_text
        server_ip[string_text] = ip

    print server_ip
    if sendres is not None:
        for activity in activity_list:
            giftList = activity.giftList
            if giftList is not None:
                for g in giftList:
                    # area_host = get_area_host(activity)
                    area_host = server_ip.get(activity.sever_code)
                    send_activity_value = {
                    'row[platform]': '1',
                    'row[area_host]': area_host,#伺服器
                    'row[reciver_name][0]':activity.role_name,#角色名称
                    'row[reciver_id][0]':'',
                    'row[mail_title]':activity.mail_title,
                    'row[mail_content]':activity.mail_content,
                    'row[reason]':activity.mail_resion, #发邮件原因
                    'row[item][]':g.gift_name,
                    'row[amount][]':g.gift_count,
                    'row[equiplevel][]':'0'
                    }
                    activity_header = {'Referer': 'http://210.68.122.121/master/duoluotaitanGM/mail/singlemail/add','Host':'210.68.122.121','Origin':'http://210.68.122.121'}
                    activity_res = m_seeion.post("http://210.68.122.121/master/duoluotaitanGM/mail/singlemail/add",data=send_activity_value,headers=activity_header)
                    if activity_res is not None:
                        print "activity_res:" + activity_res.text
                        if '操作成功' in activity_res.text:
                            print 'ok'


# def get_area_host(activity):
#     server_code = activity.sever_code
#     area_host = 'http://47.89.16.15:51050/'
#     if server_code == '1':
#         area_host = 'http://47.89.16.15:51050/'
#     elif server_code == '2':
#         area_host = 'http://47.89.16.15:51050/'
#     elif server_code == '3':
#         area_host = 'http://47.52.21.158:51050/'
#     elif server_code == '4':
#         area_host = 'http://47.52.24.110:51050/'
#     elif server_code == '5':
#         area_host = 'http://47.90.124.240:51050/'
#     elif server_code == '6':
#         area_host = 'http://47.52.17.109:51050/'
#     elif server_code == '7':
#         area_host = 'http://47.89.23.71:51050/'
#     elif server_code == '8':
#         area_host = 'http://47.89.23.71:51051/'
#     elif server_code == '9':
#         area_host = 'http://47.89.23.71:51052/'
#     elif server_code == '10':
#         area_host = 'http://47.90.126.21:51050/'
#     elif server_code == '11':
#         area_host = 'http://47.90.126.21:51051/'
#     elif server_code == '12':
#         area_host = 'http://47.89.16.15:51051/'
#     elif server_code == '13':
#         area_host = 'http://47.52.21.158:51051/'
#     elif server_code == '14':
#         area_host = 'http://47.52.24.110:51051/'
#     elif server_code == '15':
#         area_host = 'http://47.90.124.240:51051/'
#     elif server_code == '16':
#         area_host = 'http://47.52.17.109:51051/'
#     return area_host


def getGameAllInfo():

    login_page, session = session_login()

    # //根据每个服获取dua和在线
    all_config = AllConfig()

    if "area_selected_id=" in login_page.text:
        re_server_list = re.compile('area_selected_id=[\w]{0,5}')  # 判断是否为中文的正则表达式
        server_list = re_server_list.findall(login_page.text)  # 使用正则表达获取中文
        # print str
        if server_list:

            for s in server_list:
                server_list_split = s.split('=')
                # print server_list_split[1]
                all_config.sever_list.append(server_list_split[1])
            # print all_config.server_info_list

    # 获取每个服务器的在线，dau
    for v in all_config.sever_list:
        print v
        serverinfotemp = getServerInfo(session,v)
        if serverinfotemp is not None:
            all_config.server_info_list.append(serverinfotemp)


    #获取每个服务器的实时在线
    realtime(session,all_config)
    # print onlinecfg

    payment(session,all_config)
    getAllPay(session,all_config)

    total_dau=0
    total_current_online=0
    total_register=0
    game_info = '伺服器    DAU     在线人数CCU     注册数用户数     ios/google储值\n'
    game_info_s10 = ''
    for als in all_config.server_info_list:
        # print als.toStr()
        if als.login_roles == '':
            pass
        else:
            total_dau = total_dau + int(als.login_roles)

        if als.current_online == '':
            pass
        else:
            total_current_online = total_current_online + int(als.current_online)

        if als.register_roles == '':
            pass
        else:
            total_register = total_register + int(als.register_roles)

        if int(als.sever_id) > 10:
            game_info_s10 = game_info_s10 + "S " + als.sever_id + "       " + als.login_roles + "         " + als.current_online + '            ' + als.register_roles + '              ' + str( als.pays) + '\n'
        else:
            game_info = game_info + "S " + als.sever_id + "       " + als.login_roles + "         " + als.current_online + '            ' + als.register_roles + '              ' + str(als.pays) + '\n'

    game_info_huizong = 'DAU汇总:' + str(total_dau)  + "       在线人数汇总:" + str(total_current_online) + \
    '       注册汇总:' + str(total_register) + "\nMYCARD:" + all_config.others_pay + "      储值汇总:" + all_config.all_pay + "      储值人数:" + all_config.pay_persions + '\n新增付费率:' + all_config.new_pay_rate + '       活跃付费率:' + all_config.active_pay_rate + '        ARPPU:' + all_config.pay_arpu

    lvt_str = 'LTV数据如下：\n'
    for s in all_config.server_info_list:
        m = int(s.sever_id)
        if m > 12 :
            payment_ltv(session, all_config, s.sever_id)
            # print 'ltv:' + str(s.ltv_pay)
            if s.ltv_pay > 0 and s.allRegister > 0:
                lvt_str = lvt_str + "S" + s.sever_id + " : 累计储值总额: " + str(s.ltv_pay) + "       累计注册: " + str(s.allRegister) + "     LTV(USD)  : " + str(round(s.ltv_pay / s.allRegister,2)) + "\n"

    print lvt_str
    return game_info,game_info_s10,game_info_huizong,lvt_str
    # return '','',''


def session_login():
    # 使用登录cookie信息
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='gl_cookies')
    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("Cookie 未能加载")
    url = "http://210.68.122.121//master/duoluotaitanGM/index/login/"
    url1 = "http://210.68.122.121//master/duoluotaitanGM/index/login/?url=http://210.68.122.121/master/duoluotaitanGM/index"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        ,
        # 'Cookie': 'PHPSESSID=d7ivboe6vm67a8r0all3mrp5a3',
        'Host': '210.68.122.121',
        'Referer': url1
        }
    session.get(url1, headers=headers)
    # 不需要验证码直接登录成功

    values = {'username': 'fl_op1',
              'password': '123456',
              'submitid': '提交'}
    product_cookies(session)

    login_page = session.post(url, data=values, headers=headers)

    session.cookies.save()
    return login_page, session


def getGameDataInfoBeanGl():

    login_page, session = session_login()

    # //根据每个服获取dua和在线
    all_config = AllConfig()

    if "area_selected_id=" in login_page.text:
        re_server_list = re.compile('area_selected_id=[\w]{0,5}')  # 判断是否为中文的正则表达式
        server_list = re_server_list.findall(login_page.text)  # 使用正则表达获取中文
        # print str
        if server_list:

            for s in server_list:
                server_list_split = s.split('=')
                # print server_list_split[1]
                all_config.sever_list.append(server_list_split[1])
            # print all_config.server_info_list

    # 获取每个服务器的在线，dau
    for v in all_config.sever_list:
        print v
        serverinfotemp = getServerInfo(session,v)
        if serverinfotemp is not None:
            all_config.server_info_list.append(serverinfotemp)


    #获取每个服务器的实时在线
    realtime(session,all_config)
    # print onlinecfg
    payment(session, all_config)
    getAllPay(session, all_config)

    f = xlwt.Workbook()  # 创建工作簿

    '''
    创建第一个sheet:
      sheet1
    '''
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    total_dau = all_config.server_info_list[0].login_roles
    total_current_online = 0
    total_register =  all_config.server_info_list[0].register_roles
    # 生成第一行

    role_game_title = [u'别惹萌萌哒英文版 %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))]
    sheet1.write_merge(0, 0, 0, 7)
    write_row = 0
    sheet1.write(write_row, 0, role_game_title,  set_style('Times New Roman', 220, True))
    write_row = write_row + 1
    row0_title = [u'伺服器', u'DAU ', u'在线人数CCU', u'注册数用户数', u'ios/google储值', u'累计储值总额', u'累计注册', u'LTV(USD)']
    for i in range(0, len(row0_title)):
        # sheet1.col(i).width = 0x0d00
        sheet1.write(write_row, i, row0_title[i], set_style('Times New Roman', 220, True))

    write_row = write_row + 1
    style = create_wrap_centre()
    s_len = len(all_config.server_info_list)
    for j in range(s_len):
        als = all_config.server_info_list[j]
        # if als.login_roles == '':
        #     pass
        # else:
        #     total_dau = total_dau + int(als.login_roles)

        if als.current_online == '':
            pass
        else:
            total_current_online = total_current_online + int(als.current_online)

        # if als.register_roles == '':
        #     pass
        # else:
        #     total_register = total_register + int(als.register_roles)

        s_total_pay = '-'
        s_total_register = '-'
        s_ltv = '-'

        m = int(als.sever_id)
        if m == 1:
            payment_ltv(session, all_config, als.sever_id)
            # print 'ltv:' + str(s.ltv_pay)
            if als.ltv_pay > 0 and als.allRegister > 0:
                # lvt_str = lvt_str + "S" + als.sever_id + " : 累计储值总额: " + str(als.ltv_pay) + "       累计注册: " + str(
                #     s.allRegister) + "     LTV(USD)  : " + str(round(s.ltv_pay / s.allRegister, 2)) + "\n"
                s_total_pay = str(als.ltv_pay)
                s_total_register = str(als.allRegister)
                s_ltv = str(round(als.ltv_pay / als.allRegister, 2))

        if m != 1:
            als.login_roles = '-'
            als.register_roles = '-'
            als.s_total_register = '-'
            als.s_ltv = '-'
        row0_info = [als.sever_id, als.login_roles, als.current_online, als.register_roles, str(als.pays), s_total_pay, s_total_register, s_ltv]
        for i in range(0, len(row0_info)):
            sheet1.write(write_row, i, row0_info[i], style)
        write_row = write_row + 1

    # game_info_huizong = 'DAU汇总:' + str(total_dau) + "       在线人数汇总:" + str(total_current_online) + \
    #                     '       注册汇总:' + str(
    #     total_register) + "\nMYCARD:" + all_config.others_pay + "      储值汇总:" + all_config.all_pay + "      储值人数:" + all_config.pay_persions + '\n新增付费率:' + all_config.new_pay_rate + '       活跃付费率:' + all_config.active_pay_rate + '        ARPPU:' + all_config.pay_arpu

    row_title_huizong = [u'汇总', str(total_dau), str(total_current_online), str(total_register), all_config.all_pay]
    aaa = [u'新增付费率:' + all_config.new_pay_rate, u'活跃付费率:' + all_config.active_pay_rate, u'ARPPU:' + all_config.pay_arpu]

    for i in range(0, len(row_title_huizong)):
        sheet1.write(write_row, i, row_title_huizong[i], style)
    write_row = write_row + 1
    for i in range(0, len(aaa)):
        sheet1.write(write_row, i, aaa[i], style)
    write_row = write_row + 1
    f.save('E:\\jingling\\brmmd_gl_baoshu.xls')  # 保存文件

    return all_config


if __name__ == '__main__':
    getGameDataInfoBeanGl()