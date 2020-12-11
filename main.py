# -*- coding: utf-8 -*-
from settings import *
import time
from queue import Queue
from threading import Thread
import threading
from read_excel import read_excel
from write_csv import create_csv
from compile_js import get_cookie
import requests
from get_proxies import get_proxies as get_xdaili
from read_excel import split_sum_list
from find_map import find_zt, find_diqu
from write_csv import write_excel


def if_put_ip(func):
    def wrapper(*args, **kwargs):
        # 判断是否需要加IP 队列小于线程数就加
        lock.acquire()
        if ip_q.qsize() < thread_num:
            func(*args, **kwargs)
        lock.release()

    return wrapper


@if_put_ip
def put_ip():
    num = thread_num * 2
    if num > 100:
        num = 100
    while True:
        url = f'http://http.tiqu.alicdns.com/getip3?num={int(num)}&type=1&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
        try:
            proxies = requests.get(url).text
        except requests.exceptions.ProxyError:
            time.sleep(2)
            continue
        if 'false' in proxies:
            time.sleep(2)
            continue
        for ip in proxies.splitlines():
            proxies = {'https': f'https://{ip.strip()}'}
            ip_q.put(proxies)
        break


def get_proxies():
    # put_ip()
    # proxies = ip_q.get()
    # return proxies
    # -----这里是新的代理模式    --------
    return {"http": "http://forward.xdaili.cn:80", "https": "https://forward.xdaili.cn:80"}


def get_parse(url, headers, data, proxies=None):
    # print(f'ip队列总数：{ip_q.qsize()}')
    # print(f'当前IP：{proxies}')
    while True:
        try:
            headers['Proxy-Authorization'] = get_xdaili()
            response = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=10,verify=False,allow_redirects=False)
            return response
        except requests.exceptions.ProxyError:
            proxies = get_proxies()
            continue
        except Exception as e:
            print(f'错误原因：{e}')
            time.sleep(5)
            continue


def set_cookie(data_form_str, proxies):
    cookie = get_cookie(data_form_str)
    headers['cookie'] = cookie
    response = get_parse(url, headers=headers, data=data_form_str, proxies=proxies)
    if response:
        response = response.json()
        print(f'msg的值为：{response["msg"]}')
        return response


def get_z1(z1,tianshu,index):
    if z1:
        try:
            z1 = z1[index]
            shijian = z1['a']
            wuliu = ','.join([z1['c'],z1['z']])
            # wuliu = z1['d'] + "," + z1['z']
        except:
            shijian = ""
            wuliu = ""
    else:
        shijian = ""
        wuliu = ""
    return shijian,wuliu


def parse_response(response, fc, proxies):
    print(f'response:{response}')
    # no_response = []
    for sum_track in response['dat']:
        track = sum_track['track']
        # print(f'track:{track}')
        if sum_track['track']:
            danhao = sum_track['no']
            start_diqu = track['b']
            stop_diqu = track['c']
            start_diqu = find_diqu(start_diqu)
            stop_diqu = find_diqu(stop_diqu)
            zt = track['e']
            tianshu = track['f']
            if zt == '40':  # 10表示运输途中
                tianshu = f'({tianshu})天'
            else:
                tianshu = ""
            z1 = track['z1']
            # if z1:
            #     z1 = z1[-1]
            #     shijian = z1['a']
            #     wuliu = z1['c'] + "," + z1['z']
            #     zt = find_zt(zt)
            #     zt = f'{zt}{tianshu}'
            # else:
            #     zt = find_zt(zt)
            #     shijian = ""
            #     wuliu = ""
            start_sj, start_wuliu = get_z1(z1,tianshu,-1)
            er_sj, er_wuliu = get_z1(z1,tianshu,-2)
            stop_sj, stop_wuliu = get_z1(z1,tianshu,0)
            zt = find_zt(zt)
            if start_sj:
                zt = f"{zt}{tianshu}"
            if 'in' in stop_wuliu:
                stop_wuliu = stop_wuliu.split("in")[-1]
            lock.acquire()
            write_excel(f"'{danhao}", zt, start_diqu, stop_diqu, start_sj, start_wuliu,er_sj, er_wuliu,stop_sj, stop_wuliu)
            lock.release()
        else:
            dh_q.put(sum_track['no'])
            # 没有请求到，要重新换一次  不需要更换cookie     直接请求
            # 太麻烦了  我直接重新请求一次  毕竟网速不好不是经常的
    #         no_response.append(sum_track['no'])
    # new_list = split_sum_list(no_response)
    # # new_list可能为0
    # if new_list:
    #     start_request(new_list, fc, proxies)


# 最开始的查询列表
# root_list = read_excel(filename)
# def if_get_proxies():
#     # 如果msg的值为uip则需要加IP
#     proxies = get_proxies()
#     return proxies


def start_request(root_list, fc, proxies=None):
    # for num_list in root_list:
    data_form['data'].clear()  # 清空data的值
    for num in root_list:
        if num:
            data_form['data'].append({"num": str(num).split('.')[0], "fc": fc, "sc": 0})
    data_form_str = str(data_form).replace("'", '"')
    print(f'data_form_str:{data_form_str}')

    while True:
        response = set_cookie(data_form_str, proxies)
        if response['msg'] == 'uIP':
            proxies = get_proxies()
            continue
        break
    parse_response(response, fc, proxies)



def input_main():
    fc = input(f'''输入要查询的物流(默认自动识别)：
                    1. 美国
                    2.DHL
                    3.新加坡
                    4.比利时
                    5.fedex
                    请输入：''')

    if fc == "1":
        fc = '21051'
    elif fc == '2':
        fc = "100001"
    elif fc == '3':
        fc = "19131"
    elif fc == '4':
        fc = "02061"
    elif fc == '5':
        fc = "100003"
    else:
        fc = '0'
    return fc


def int_thread(num):
    try:
        num = int(num)
        return num
    except ValueError:
        raise Exception(f'请输入一个整数')


def main_new():
    while not dh_q.empty():
        num = 40
        # print(f'测试')
        lock.acquire()  # 加锁
        if dh_q.qsize() < num:
            num = dh_q.qsize()
        root_list = []
        for i in range(num):
            dh = dh_q.get()
            root_list.append(dh)
        lock.release()  # 解锁
        proxies = get_proxies()
        start_request(root_list, fc, proxies)



def start_thread():
    t_list = []
    for i in range(thread_num):
        t = Thread(target=main_new)
        t_list.append(t)
    for t in t_list:
        # t.setDaemon(True)
        t.start()
    for t in t_list:
        t.join()


def main():
    root_list = read_excel(filename)  # 读取需要查询的单号
    for i in root_list:
        dh_q.put(i)
    print(f"总数量：{dh_q.qsize()}")
    create_csv()  # 创建表格
    # put_ip()  # IP入队列
    start_thread()

    # proxies = get_proxies()  # 开始就换IP  不用自己的IP
    # start_request(root_list, fc, proxies)  # 开始爬取


if __name__ == '__main__':
    # 最开始的查询列表
    # 准备工作
    fc = input_main()  # 获取物流商
    thread_num = input(f'请输入线程数(建议小于10)：')
    thread_num = int_thread(thread_num)
    # 启动两个队列
    dh_q = Queue()
    ip_q = Queue()
    lock = threading.Lock()
    main()
