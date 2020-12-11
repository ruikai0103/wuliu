from queue import Queue
import requests
import time

ip_q = Queue()
data_form = {
    "data": [],
    "guid": "",
    "timeZoneOffset": -480
}


def put_ip_(root_list):
    print(f'root_list::{root_list}')
    # for num_list in root_list:
    data_form['data'].clear()  # 清空data的值
    for num in root_list:
        if num:
            data_form['data'].append({"num": str(num).split('.')[0], "fc": 'fc', "sc": 0})
    data_form_str = str(data_form).replace("'", '"')
    print(f'data_form_str:{data_form_str}')


# num = 30
# root_list = []
# for i in range(num):
#     dh = i
#     root_list.append(dh)
# put_ip(root_list)
def put_ip():
    while True:
        url = f'http://http.tiqu.alicdns.com/getip3?num={10}&type=1&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
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
            print(f'IP:{proxies}')
        break


a = "qqq"
print(a.split("in"))

time.sleep(2)
