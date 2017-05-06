#-*- coding: UTF-8 -*-

from pachong import *
from activitymmd.excelutil import *

if __name__ == '__main__':
    # sendActivityWuPin(None)
    excel_path = 'E:\\55huodong.xlsx'
    # excel_path = 'E:\\test.xlsx'
    activitys_list = readExcel(excel_path)

    # if activitys_list is not None:
    #     sendActivityWuPin(activitys_list)
