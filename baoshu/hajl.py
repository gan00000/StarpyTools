#-*- coding: UTF-8 -*-
import sys
import time
import types
import simplejson as json
import xlwt
from bs4 import BeautifulSoup

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
    userlogin = Login2()
    loginPage = 'http://jllrcsss-tw.starb168.com/gameManager/index.jsp'
    loginPostUrl = 'http://jllrcsss-tw.starb168.com/gameManager/login.do'
    postVaule = {
        'username': 'csstarby3',
        'password': '123456'
    }
    headers = {
        'Referer': 'http://jllrcsss-tw.starb168.com/gameManager/index.jsp',
        'Cookie': 'JSESSIONID=9EF250762D948835023FB51184352530',
        'Host': 'jllrcsss-tw.starb168.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }

    # menupage,urllib2 = userlogin.login(loginPostUrl,postVaule,headers,'hajj_cookies')

    login_success_page, login_session = mLogin.session_login(loginPage, loginPostUrl, postVaule, headers,'hajj_cookies')

    menupage = login_session.get('http://jllrcsss-tw.starb168.com/gameManager/menu.jsp',headers= headers)
    # print menupage.text

    listSmsg = showDailyReport(login_session,headers)

    writeExcel(listSmsg)


def writeExcel(listSmsg):

    title = [u'区服', u'新增账号', u'角色登录数', u'新增付费角色数', u'新增收入', u'新增付费比', u'新增ARPPU', u'全部付费角色数', u'当日全部收入', u'付费率', u'ARPPU',
             u'LTV']
    excel = xlwt.Workbook()  # 创建工作簿
    sheet1 = excel.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    role_game_title = [u'精灵猎人 %s' % (time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))]
    sheet1.write_merge(0, 0, 0, len(title))
    write_row = 0
    sheet1.write(write_row, 0, role_game_title, set_style('Times New Roman', 220, True))
    write_row = write_row + 1

    for i in range(0, len(title)):
        sheet1.write(write_row, i, title[i], set_style('Times New Roman', 220, True))
    write_row = write_row + 1
    style = create_wrap_centre()
    for s in listSmsg:
        content = [s.serverName, s.newRole, s.roleLogin, s.newPayRole, s.newPay, s.newPayRate, s.newARPPU,
                   s.totalRolePay, s.totalPay,s.payPercent, s.arppu,s.ltv]
        for i in range(0, len(content)):
            sheet1.write(write_row, i, content[i], style)
        write_row = write_row + 1

    excel.save('E:\\jingling\\hajl_baoshu.xls')  # 保存文件



def showDailyReport(loginSession,headers):
    url = 'http://jllrcsss-tw.starb168.com/gameManager/view/pay/showDailyReport.jsp'
    loginSession.get(url,headers = headers)

    showDailyReportDo = 'http://jllrcsss-tw.starb168.com/gameManager/pay/showDailyReport.do'

    serverIds = getServers(headers, loginSession)#获取所有伺服器id
    listSmsg = []
    if serverIds:
        print serverIds
        for a in serverIds:
            if a == 1000:
                pass
            else:
                print 'serverId:' + str(a)
                sMsg = getServerMsg(headers, loginSession, showDailyReportDo, a) #获取所有伺服器信息
                print str(sMsg.totalPay)
                listSmsg.append(sMsg)
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
            serverIds.append(serverId)
    return serverIds


def getServerMsg(headers, loginSession, showDailyReportDo,serverId):
    startTime = get_current_time() + ' 00:00:00'
    values = {
        'serverId': serverId,
        'startTime': startTime,
        'endTime': get_current_time2(),
        'gmpay': '1'
    }
    s = loginSession.post(showDailyReportDo, data=values, headers=headers)
    # print s.text
    parsed_json = json.loads(s.text)
    if parsed_json:
        serverArry = parsed_json.get('rows')
        if serverArry:
            for obj in serverArry:
                platform = obj.get('platform')
                if platform == '全平台':
                    newID = obj.get('newID')  # 新增账号
                    liveID = obj.get('liveID')  # 活跃账号
                    payUser = obj.get('payUser')  # 付费用户
                    payPercent = obj.get('payPercent')  # 付费率
                    liveARPU = obj.get('liveARPU')  # 活跃arpu
                    income = obj.get('income')  # 当日收入
                    newARPU = obj.get('newARPU')  # 新增arpu
                    payARPU = obj.get('payARPU')  # 付费arpu

                    sMsg = ServerMsg()
                    sMsg.newRole = newID
                    sMsg.newARPPU = newARPU
                    sMsg.arppu = payARPU
                    sMsg.totalPay = income
                    sMsg.totalRolePay = payUser
                    sMsg.payPercent = payPercent
                    sMsg.serverName = serverId
                    sMsg.roleLogin = liveID

                    return sMsg
    return None


if __name__ == '__main__':
    requestData()