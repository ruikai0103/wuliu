'''
打开Excel并且分割成40个一组的列表
'''
import xlrd
import sys
from math import ceil


def read_excel(filename):
    filename = f'../{filename}.xlsx'
    # filename = f'./{filename}.xlsx'
    try:
        data = xlrd.open_workbook(filename)
    except FileNotFoundError:
        print(f'文件不存在，程序3秒后退出')
        sys.exit()
    # 查看工作表
    data.sheet_names()
    table = data.sheet_by_name(data.sheet_names()[0])
    sum_list = table.col_values(0)
    sum_list = [i for i in sum_list if i != '']
    return sum_list


def split_sum_list(sum_list):
    new_list = []
    sum = 0
    for i in range(ceil(len(sum_list) / 40)):
        if sum_list[sum:sum + 40]:
            new_list.append(sum_list[sum:sum + 40])
            sum += 40
    return new_list


if __name__ == '__main__':
    filename = '200'
    root_list = read_excel(filename)
    print(root_list)