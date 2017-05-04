#-*- coding: UTF-8 -*-

class AllConfig:

    def __init__(self):
        self.time = ""
        self.sever_list = []
        self.server_info_list = []
        self.all_pay = ''
        self.guanfang_pay=''
        self.others_pay=''
        self.new_pay_rate=''
        self.active_pay_rate=''
        self.pay_persions = ''
        self.pay_arpu = ''

    def toStr(self):
        return 'all_pay:' + self.all_pay + ' guanfang_pay:' + self.guanfang_pay + ' others_pay:' + self.others_pay + ' new_pay_rate:' + self.new_pay_rate + ' active_pay_rate:' + self.active_pay_rate
