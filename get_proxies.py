import time
import hashlib
import urllib3


def get_proxies():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    orderno = "ZF20205202306YCxov6"
    secret = "0c6e58691e9b4558b6004f14627ecc8f"

    ip = "forward.xdaili.cn"
    port = "80"

    ip_port = ip + ":" + port

    timestamp = str(int(time.time()))
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp


    string = string.encode()

    md5_string = hashlib.md5(string).hexdigest()
    sign = md5_string.upper()
    #print(sign)
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

    #print(auth)
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    # headers = {"Proxy-Authorization": auth, "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}
    # r = requests.get("https://www.ip.cn/api/index?ip=&type=0", headers=headers, proxies=proxy, verify=False,allow_redirects=False)
    return auth