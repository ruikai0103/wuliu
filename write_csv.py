from pandas import DataFrame
from settings import to_csv


def write_excel(*args):
    value = [[*args]]
    data_df = DataFrame(value)
    data_df.to_csv(to_csv, index=False, mode="a", header=False)


def create_csv():
    value_title = [['单号', '状态天数','开始地区','运输地区', '开始时间', '开始物流', '第二时间', '第二物流','当前时间', '当前物流',]]
    data_df = DataFrame(value_title)
    data_df.to_csv(to_csv, index=False, mode="a", header=False)