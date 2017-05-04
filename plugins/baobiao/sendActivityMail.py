#-*- coding: UTF-8 -*-

from pachong import *
from activitymmd.excelutil import *

excel_path = 'E:\\tetsaa.xlsx'
# excel_path = 'E:\\test.xlsx'
activitys_list = readExcel(excel_path)
print 'aaa'
if activitys_list is not None:
    sendActivityWuPin(activitys_list)

# send_activity_value = {
#         'row[platform]': '1',#伺服器
#         'row[area_host]': "dd"
#         }
#
# send_activity_value2 = {
#     'row[platform]': '1',  # 伺服器
#     'row[area_host]': "dd"
# }
#
# a = dict(send_activity_value.items() | send_activity_value2.items())
#
# for b in a:
#     print(b)