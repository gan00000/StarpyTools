#-*- coding: UTF-8 -*-

from pachong import *
import sys

from activitymmd.excelutil import *

if __name__ == '__main__':
    # sendActivityWuPin(None)
    s = sys.getdefaultencoding()
    print s
    excel_path = 'E:\\5月12日-活动发送表格.xlsx'

    activitys_list = readExcel(excel_path.encode('gbk'), 0)

    # if activitys_list is not None:
    #     sendActivityWuPin(activitys_list)