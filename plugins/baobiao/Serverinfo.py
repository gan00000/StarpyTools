#-*- coding: UTF-8 -*-

class Serverinfo:

    def __init__(self):
        self.time = ''
        self.sever_id = ''
        self.register_roles = '0'
        self.login_roles = '0'
        self.current_online = '0'
        self.pays = 0
        self.other_pays = '0'
        self.ltv_pay = 0
        self.allRegister = 0

    def toStr(self):
        return 'sever_id:' + self.sever_id + ' register_roles:' + self.register_roles + ' login_roles:' + self.login_roles + '  current_online:' +  self.current_online  + ' pays:' + str(self.pays) + '  other_pays:' + self.other_pays