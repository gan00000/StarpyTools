# _*_ coding:utf-8 _*_

'''
设置单元格样式
'''
import types

import xlwt


def set_style(name, height, bold=False):

    # style = xlwt.XFStyle()  # 初始化样式
    style = xlwt.easyxf('align: wrap on,vert centre, horiz centre;')

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()

    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


def create_wrap_centre():
    style = xlwt.easyxf('align: wrap on,vert centre, horiz centre;')
    return style

def create_wrap_centre_A():
    style = xlwt.easyxf('align: wrap on,vert centre, horiz centre;pattern: pattern solid, fore_colour light_turquoise;')
    return style
def create_wrap_centre_B():
    style = xlwt.easyxf('align: wrap on,vert centre, horiz centre;pattern: pattern solid, fore_colour light_green;')
    return style
def create_wrap_centre_C():
    style = xlwt.easyxf('align: wrap on,vert centre, horiz centre;pattern: pattern solid, fore_colour light_orange;')
    return style
def create_wrap_centre_E():
    style = xlwt.easyxf('align: wrap on,vert centre, horiz centre; pattern: pattern solid, fore_colour black;')
    font = xlwt.Font()  # 为样式创建字体
    font.colour_index = 1
    font.bold = True
    font.height = 20 * 16
    style.font = font
    return style
def create_wrap_centre_D():
    style = xlwt.easyxf('align: wrap on,vert centre, horiz centre;pattern: pattern solid, fore_colour dark_red;')
    return style

def writeExcelForGameInfo(path, title_title, listSmsg):

    title = [u'区服', u'新增账号', u'CCU',u'DAU', u'新增付费角色数', u'新增收入', u'新增付费比', u'新增ARPPU', u'全部付费角色数', u'当日全部收入', u'付费率', u'ARPPU',
             u'LTV']
    excel = xlwt.Workbook()  # 创建工作簿
    sheet1 = excel.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    role_game_title = [title_title]
    sheet1.write_merge(0, 0, 0, len(title))
    write_row = 0
    sheet1.write(write_row, 0, role_game_title, set_style('Times New Roman', 220, True))
    write_row = write_row + 1

    for i in range(0, len(title)):
        sheet1.write(write_row, i, title[i], set_style('Times New Roman', 220, True))
    write_row = write_row + 1
    style = create_wrap_centre()

    for s in listSmsg:
        content = [s.serverName, s.newRole,s.ccu, s.roleLogin, s.newPayRole, s.newPay, s.newPayRate, s.newARPPU,
                   s.totalRolePay, s.totalPay,s.payPercent, s.arppu,s.ltv]
        for i in range(0, len(content)):
            sheet1.write(write_row, i, content[i], style)
        write_row = write_row + 1

    excel.save(path)  # 保存文件

def writeExcelForGameInfo_new(path, title_title, listSmsg):

    allTitle = [u'CCU', u'DAU',u'付费人数', u'营收', u'付费率', u'ARPPU', u'LTV']
    newTitle = [ u'新增用户', u'付费人数', u'营收', u'付费率', u'ARPPU']
    dauTitle = [u'DAU',u'付费人数', u'营收', u'付费率', u'ARPPU']
    excel = xlwt.Workbook()  # 创建工作簿
    sheet1 = excel.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    style = create_wrap_centre()

    sheet1.write_merge(0, 0, 0, len(allTitle) + len(newTitle) + len(dauTitle), title_title,create_wrap_centre_E())
    write_row = 0
    write_row = write_row + 1

    # style = set_style('Times New Roman', 220, True)
    sheet1.write_merge(1, 2, 0, 0, u'区服',create_wrap_centre_D())

    style_a = create_wrap_centre_A()
    style_b = create_wrap_centre_B()
    style_c = create_wrap_centre_C()
    sheet1.write_merge(write_row, write_row, 1, len(allTitle), u'总体',style_a)
    sheet1.write_merge(write_row, write_row, len(allTitle) + 1, len(allTitle) + len(newTitle), label=u'新用户', style=style_b)
    sheet1.write_merge(write_row, write_row, len(allTitle) + len(newTitle) + 1, len(allTitle) + len(newTitle) + len(dauTitle), label=u'活跃用户', style = style_c)
    write_row = write_row + 1 

    # set_style('Times New Roman', 220, True)
    write_array(sheet1, allTitle, 2, 1, style_a)
    write_array(sheet1, newTitle, 2, len(allTitle) + 1, style_b)
    write_array(sheet1, dauTitle, 2, len(allTitle) + len(newTitle) + 1, style_c)
    write_row = write_row + 1

    for s in listSmsg:
        content = [s.serverName, s.newRole, s.ccu, s.roleLogin, s.newPayRole, s.newPay, s.newPayRate, s.newARPPU,
                   s.totalRolePay, s.totalPay, s.payPercent, s.arppu, s.ltv]
        # for i in range(0, len(content)):
        #     sheet1.write(write_row, i, content[i], style)

        sheet1.write(write_row, 0, s.serverName, style)

        sheet1.write(write_row, 1, s.ccu, style)
        sheet1.write(write_row, 2, s.roleLogin, style)
        sheet1.write(write_row, 3, s.totalRolePay, style)#所有付费角色数
        sheet1.write(write_row, 4, s.totalPay, style)#当天所有付费
        sheet1.write(write_row, 5, s.payPercent, style)#当天付费率
        sheet1.write(write_row, 6, s.arppu, style)#总arppu
        sheet1.write(write_row, 7, s.ltv, style)#ltv

        # m = len(allTitle)
        sheet1.write(write_row, 8, s.newRole, style)#新增角色
        sheet1.write(write_row, 9, s.newPayRole, style)#新增付费角色数
        sheet1.write(write_row, 10, s.newPay, style)#新增付费
        sheet1.write(write_row, 11, s.newPayRate, style)#新增付费率

        sheet1.write(write_row, 13, s.roleLogin, style)  # 活跃付费率
        if s.totalRolePay == '-' or s.newPayRole == '-':
            pass
        else:
            sheet1.write(write_row, 14, s.totalRolePay - s.newPayRole, style)  # 活跃付费人数
        sheet1.write(write_row, 15, s.totalPay , style)  # 活跃营收
        # sheet1.write(write_row, 16, s.newPayRate, style)  # 活跃付费率
        # sheet1.write(write_row, 17, s.newPayRate, style)  # 活跃arppu

        if s.newPay and s.newPayRole:
            try:
                new_arppu = round(s.newPay / s.newPayRol,2)
                sheet1.write(write_row, 11, new_arppu, style)  # 新增Arppu
            except:
                pass

        write_row = write_row + 1

    excel.save(path)  # 保存文件

def write_array(sheet1, content_array, r, c, style):

    for i in range(0, len(content_array)):
        sheet1.write(r, c, content_array[i], style)
        c = c + 1

# 写excel
def write_excel():

    f = xlwt.Workbook()  # 创建工作簿

    '''
    创建第一个sheet:
      sheet1
    '''
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'业务', u'状态', u'北京', u'上海', u'广州', u'深圳', u'状态小计', u'合计']

    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.col(i).width = 0x0d00 * 2
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))

    # # 生成第一列和最后一列(合并4行)
    # i, j = 1, 0
    # while i < 4 * len(column0) and j < len(column0):
    #     sheet1.write_merge(i, i + 3, 0, 0, column0[j], set_style('Arial', 220, True))  # 第一列
    #     sheet1.write_merge(i, i + 3, 7, 7)  # 最后一列"合计"
    #     i += 4
    #     j += 1
    #
    # sheet1.write_merge(21, 21, 0, 1, u'合计', set_style('Times New Roman', 220, True))
    #
    # # 生成第二列
    # i = 0
    # while i < 4 * len(column0):
    #     for j in range(0, len(status)):
    #         sheet1.write(j + i + 1, 1, status[j])
    #     i += 4
    sheet1.write_merge(2, 2, 0, 7)
    f.save('F:\\分割123saaa.xls')  # 保存文件


if __name__ == '__main__':
    # generate_workbook()
    # read_excel()
    # write_excel()
    writeExcelForGameInfo_new(u'/Users/gan/Desktop/test.xls',u'大家啊看',None)
    print u'创建xlsx文件成功'
