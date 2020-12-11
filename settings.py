url = 'https://t.17track.net/restapi/track'

headers = {
    "Host": "t.17track.net",
    "Connection": "keep-alive",
    "Content-Length": "1966",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://t.17track.net",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://t.17track.net/zh-cn",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
data_form = {
    "data": [],
    "guid": "",
    "timeZoneOffset": -480
}

# filename = 'gongzuo8'
filename = input(f'输入文件名(xlsx结尾的，不需要后缀)：')

to_csv = f'../{filename}副本.csv'
