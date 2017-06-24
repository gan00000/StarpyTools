# _*_ coding:utf-8 _*_

import types

from baoshu.ServerMsg import ServerMsg
import os


def sumSmsg(listSmsg):
    allSmsg = ServerMsg()
    allNewRole = 0
    ccuAll = 0
    roleLoginALL = 0
    newPayRole = 0
    newIncome = 0
    newArppu = 0
    allPayRole = 0
    allIncome = 0
    allArppu = 0
    allLTV = 0
    payPercentAll = 0

    for s in listSmsg:

        allNewRole = allNewRole + int(s.newRole)
        if not s.ccu == '-':
            ccuAll = ccuAll + s.ccu
        if not s.roleLogin == '-':
            roleLoginALL = roleLoginALL + int(s.roleLogin)
        if not s.newPayRole == '-':
            newPayRole = newPayRole + int(s.newPayRole)
        if not s.newPay == '-':
            newIncome = newIncome + float(s.newPay)
        if not s.newARPPU == '-':
            newArppu = newArppu + float(s.newARPPU)
        if not s.totalRolePay == '-':
            allPayRole = allPayRole + float(s.totalRolePay)
        if not s.totalPay == '-':
            allIncome = allIncome + float(s.totalPay)
        try:
            if type(s.arppu) is types.StringType:
                pass
            else:
                allArppu = allArppu + float(s.arppu)
            if not s.ltv == '-':
                allLTV = allLTV + float(s.ltv)
            if not s.payPercent == '-':
                payPercentAll = payPercentAll + float(s.payPercent)

        except:
            pass

    allSmsg.serverName = u'汇总'
    allSmsg.newRole = allNewRole
    allSmsg.ccu = ccuAll
    allSmsg.roleLogin = roleLoginALL
    allSmsg.totalRolePay = allPayRole
    allSmsg.totalPay = allIncome
    listSmsg.append(allSmsg)
    # huizong = [u'汇总', allNewRole,ccuAll, roleLoginALL, '-', '-', '-', '-', allPayRole, allIncome, '-', '-', '-']
    return listSmsg


previousListSmsgArray = {}

def doErrorMsg(errorLogFile, listSmsg):
    errrFile = open(errorLogFile, 'w')
    errrFile.write('')
    errrFile.close()

    global previousListSmsgArray
    if previousListSmsgArray and listSmsg:
        errorLog = ''
        try:
            previousListSmsg = previousListSmsgArray.get(listSmsg[0].gameName)
            if previousListSmsg:
                for theS in listSmsg:
                    theSName = theS.serverName
                    if theSName == u'汇总':
                        break

                    for preS in previousListSmsg:
                        if preS.serverName == theSName:
                            if float(theS.totalPay) <= float(preS.totalPay):
                                # 储值无增长报警
                                errorLog = errorLog + '警告：' + theS.gameName + ' 伺服器: ' + theSName + " 储值 与上一次报数无增长\n"

                            if int(theS.roleLogin) <= int(preS.roleLogin):
                                # DAU无增长报警
                                errorLog = errorLog + '警告：' + theS.gameName + ' 伺服器: ' + theSName + " DAU 与上一次报数无增长\n"

                            if preS.ccu == '0':
                                # 在线为0报警
                                errorLog = errorLog + '警告：' + theS.gameName + ' 伺服器: ' + theSName + " 在线为0\n"

                if not errorLog == '':
                    errrFile = open(errorLogFile, 'w')
                    errrFile.write(errorLog)
                    errrFile.close()
        except:
            pass
    previousListSmsgArray[listSmsg[0].gameName] = listSmsg

