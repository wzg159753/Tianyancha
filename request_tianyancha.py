from datetime import datetime
from requests.sessions import cookiejar_from_dict
import requests
import execjs


with open('test.js', 'r') as f:
    result = execjs.compile(f.read())

suid = result.call('get_suid')
print(f'suid={suid}')


session = requests.Session()

headers = {
    'Host': 'www.tianyancha.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

session.headers = headers

# 第一次请求
resp = session.get('https://www.tianyancha.com/')
resp.encoding = 'UTF-8'

print(resp.cookies)
cookie_str = ''
for cookie in list(resp.cookies):
    cookie_str += f'{cookie.name}={cookie.value}'

session.headers.update({
    'Cookie': cookie_str
})

# print(headers)
# session.cookies.update(resp.cookies)

# img = session.get(f'https://hm.baidu.com/hm.gif?cc=1&ck=1&cl=24-bit&ds=1536x864&vl=710&ep=89559%2C9969&et=3&ja=0&ln=zh-cn&lo=0&lt={int(datetime.now().timestamp() * 1000)}&rnd=1917054682&si=e92c8d65d92d534b0fc290df538b4758&v=1.2.51&lv=2&sn=1527')
# print(img)
#
params = {
    '_': int(datetime.now().timestamp() * 1000)
}
url = 'https://www.tianyancha.com/claim/getLabels.json'

resp2 = session.get(url)
#
# session.cookies.update(resp2.cookies)
#
for cookie1 in list(resp2.cookies):
    cookie_str += '; ' + f'{cookie1.name}={cookie1.value}'

session.headers.update({
    'Cookie': cookie_str
})
# cookies = {
#     'ssuid': suid,
#     'bannerFlag': 'undefined'
# }

# requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
# session.cookies.update(cookies)
# print(session.cookies[0])

resp3 = session.get(url=f'https://www.tianyancha.com/newest.html?ps=40&_={int(datetime.now().timestamp() * 1000)}')
print(session.headers)
# resp3 = requests.get(f'https://www.tianyancha.com/newest.html?ps=40&_={int(datetime.now().timestamp() * 1000)}', headers=headers)
# print(resp3.text)
print(resp3.cookies)

