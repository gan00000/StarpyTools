#-*- coding: UTF-8 -*-


class ServerMsg:

    def __init__(self):
        self.data = ''
        self.serverName = ''
        self.newRole = '0'
        self.roleLogin = '-' #活跃用户DAU
        self.newPayRole = '-'
        self.newPay = '-'
        self.newPayRate = '-'
        self.newARPPU = '-'

        self.payPercent = '-'
        self.ccu = '-' #在线用户

        self.totalRolePay = '-'
        self.totalPay = '-'

        self.arppu = '-'

        self.ltv = '-'
        self.allDayReg = 0
        self.allDayPay = 0