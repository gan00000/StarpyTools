#-*- coding: UTF-8 -*-
import sys

from activitymmd.excelutil import *
from baoshu import hajl

if __name__ == '__main__':
    # sendActivityWuPin(None)
    s = sys.getdefaultencoding()
    print s
    excel_path = 'E:\\6月23日-brmmd-活动发送表格.xlsx'

    activitys_list = readExcel(excel_path.encode('gbk'), 0)
    hajl.sendWupinByEmail(activitys_list)

    # if activitys_list is not None:
    #     sendActivityWuPin(activitys_list)
