#-*- coding: UTF-8 -*-


class ServerMsg:

    def __init__(self):
        self.gameName = '' #游戏名字
        self.data = ''
        self.serverName = ''
        self.serverId = ''
        self.newRole = '0' #新增用户数
        self.roleLogin = '-' #活跃用户DAU
        self.newPayRole = '-'
        self.newPay = '-'
        self.newPayRate = '-'
        self.newARPPU = '-'

        self.payPercent = '-'
        self.ccu = '-' #在线用户

        self.totalRolePay = '-' #当天所有付费角色数
        self.totalPay = '0'#当天所有付费

        self.arppu = '-'

        self.ltv = '-'
        self.allDayReg = 0  #所有注册，用于计算ltv
        self.allDayPay = 0 #所有储值，用于计算ltv