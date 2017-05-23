#coding=utf-8
import xlrd
import collections
from activitybean import *
from gitinfo import *
import os

def writeexcel(file_name, t_list):
    #打开excel
    data = xlrd.open_workbook(file_name) #注意这里的workbook首字母是小写
    #查看文件中包含sheet的名称
    #data.sheet_names()
    #得到第一个工作表，或者通过索引顺序 或 工作表名称
    table = data.sheets()[0]
    # table = data.sheet_by_index(0)
    # table = data.sheet_by_name(u'Sheet1')
    # #获取行数和列数
    # nrows = table.nrows
    # ncols = table.ncols
    # #获取整行和整列的值（数组）
    # table.row_values(i)
    # table.col_values(i)
    # #循环行,得到索引的列表
    # for rownum in range(table.nrows):
    # print table.row_values(rownum)
    # #单元格
    # cell_A1 = table.cell(0,0).value
    # cell_C4 = table.cell(2,3).value
    # #分别使用行列索引
    # cell_A1 = table.row(0)[0].value
    # cell_A2 = table.col(1)[0].value
    #简单的写入
    row = 0
    col = 0
    ctype = 1  # 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error

    for v in t_list:
        value = v
        xf = 0 # 扩展的格式化 (默认是0)
        table.put_cell(row, col, ctype, value, xf)
        # table.cell(0,0) # 文本:u'lixiaoluo'
        table.cell(row,0).value = v # 'lixiaoluo'
        row = row + 1

def readExcel(file_name,sheet):

    if os.path.exists(file_name) is not True:
        print 'excel不存在'
        return

    # 打开excel
    data = xlrd.open_workbook(file_name,"rb")  # 注意这里的workbook首字母是小写
    # 查看文件中包含sheet的名称
    # data.sheet_names()
    # 得到第一个工作表，或者通过索引顺序 或 工作表名称

    activitybean_list = []

    table = data.sheets()[sheet]

    # for table in tables:

    # #获取行数和列数
    nrows = table.nrows
    ncols = table.ncols
    print ncols
    print nrows
    # 循环行列表数据
    # request必须配置

    for i in range(nrows):
        if i == 0:
            pass
        else:
            activitybean_info = activitybean()
            sever_code = table.cell(i, 0).value
            role_name = table.cell(i, 1).value
            mail_title = table.cell(i, 2).value
            mail_content = table.cell(i, 3).value
            mail_resion = table.cell(i, 4).value

            sever_code_str = str(int(sever_code))
            activitybean_info.sever_code = sever_code_str
            activitybean_info.role_name = role_name
            activitybean_info.mail_title = mail_title
            activitybean_info.mail_content = mail_content
            activitybean_info.mail_resion = mail_resion
            print role_name
            items_str = table.cell(i, 5).value
            if items_str == '':
                pass
            else:
                items_lsit = items_str.split(';')
                for item in items_lsit:
                    if item == '' or item is None:
                        pass
                    else:

                        gitinfo_temp = gitinfo()
                        git_name_num = item.split(',')
                        git_name = git_name_num[0]

                        git_num = git_name_num[1]
                        print git_name
                        print git_num
                        gitinfo_temp.gift_name = git_name
                        gitinfo_temp.gift_count = git_num
                        activitybean_info.giftList.append(gitinfo_temp)

                activitybean_list.append(activitybean_info)

    return activitybean_list