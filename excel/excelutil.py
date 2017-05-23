# _*_ coding:utf-8 _*_

'''
设置单元格样式
'''
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

    f.save('F:\\123s.xls')  # 保存文件


if __name__ == '__main__':
    # generate_workbook()
    # read_excel()
    write_excel()
    print u'创建demo.xlsx文件成功'