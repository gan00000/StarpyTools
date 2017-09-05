#-*- coding: UTF-8 -*-
import sys

from activitymmd.excelutil import *
from baoshu import hajl
import pachonggl

if __name__ == '__main__':
    # sendActivityWuPin(None)
    s = sys.getdefaultencoding()
    print s
    excel_path = u'E:\\9.3日-gbbrmmd-活动发送表格.xlsx'

    activitys_list = readExcel(excel_path, 0)
    # hajl.sendWupinByEmail(activitys_list)

    if activitys_list is not None:
        # pachong.sendActivityWuPin(activitys_list)
        # pachonggl.sendActivityWuPin(activitys_list)
        pass
