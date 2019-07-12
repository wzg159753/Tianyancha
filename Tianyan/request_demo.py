import json
from urllib import parse
import base64
from datetime import datetime
from requests.sessions import cookiejar_from_dict
import requests
import execjs


with open('../test.js', 'r') as f:
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

# 获取HMSACCOUNT的cookie
a = session.get(f'https://hm.baidu.com/hm.gif?cc=1&ck=1&cl=24-bit&ds=1536x864&vl=410&ep=14806%2C4421&et=3&ja=0&ln=zh-cn&lo=0&lt={str(int(datetime.now().timestamp() * 1000))}&rnd=966120243&si=e92c8d65d92d534b0fc290df538b4758&su=https%3A%2F%2Fwww.tianyancha.com%2F&v=1.2.51&lv=2&sn=16695')
# print(a.cookies)

session.headers = headers
# 第一次请求
# 获取aliyun的cookie
resp = session.get('https://www.tianyancha.com/')
resp.encoding = 'UTF-8'
# print(resp.cookies)

# 自己添加cookie
cookie = {
    'ssuid': str(suid),
    'bannerFlag': 'undefined'
}
cookies = cookiejar_from_dict(cookie)
session.cookies.update(cookies)

params1 = {
    'ps': '40',
    '_': str(int(datetime.now().timestamp() * 1000))
}

# 获取csrftoken，TYCID，undefined的cookie
resp4 = session.get(f'https://www.tianyancha.com/user/getHomeNavHeader.html?_={str(int(datetime.now().timestamp() * 1000))}')
# print(resp4.cookies)



headers = {
    'Host': 'hm.baidu.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://www.tianyancha.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'HMACCOUNT=1C9D23BB0EE1C5C8',
    'If-None-Match': 'e447e132e1cff195b3cf46d79cd3b51c'
}
ttt = session.get('https://hm.baidu.com/hm.js?e92c8d65d92d534b0fc290df538b4758', headers=headers)
print(ttt.cookies)

tbt = session.get('https://sp0.baidu.com/9_Q4simg2RQJ8t7jm9iCKT-xh_/s.gif?l=https://www.tianyancha.com/', headers=headers)
print(tbt.cookies)


# {"data":{"claimEditPoint":"0","explainPoint":"0","integrity":"14%","state":"3","surday":"188","announcementPoint":"0","vipManager":"0","onum":"5","monitorUnreadCount":"56","discussCommendCount":"1","claimPoint":"0","token":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzM3NTM1ODU4MSIsImlhdCI6MTU2MjU2ODg1OSwiZXhwIjoxNTk0MTA0ODU5fQ.cu2VYzz93n4hz8i1d6IOXhj5BBx5S44QTRk9JzZ0mLEY_X0vy23LlCPClzy4CvNbU1McGGlOgyhyev7YKbOkKw","vipToTime":"1578728208870","redPoint":"0","myAnswerCount":"0","myQuestionCount":"0","signUp":"0","nickname":"薇诺娜·瑞德","privateMessagePointWeb":"0","privateMessagePoint":"0","isClaim":"0","companyName":"信联资信服务有限公司北京分公司","isExpired":"0","pleaseAnswerCount":"1","vnum":"0","bizCardUnread":"0","mobile":"13375358581"},"state":"ok"}
s = '{"claimEditPoint":"0","explainPoint":"0","integrity":"14%","state":"3","surday":"188","announcementPoint":"0","vipManager":"0","onum":"5","monitorUnreadCount":"56","discussCommendCount":"1","claimPoint":"0","token":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzM3NTM1ODU4MSIsImlhdCI6MTU2MjU2ODg1OSwiZXhwIjoxNTk0MTA0ODU5fQ.cu2VYzz93n4hz8i1d6IOXhj5BBx5S44QTRk9JzZ0mLEY_X0vy23LlCPClzy4CvNbU1McGGlOgyhyev7YKbOkKw","vipToTime":"1578728208870","redPoint":"0","myAnswerCount":"0","myQuestionCount":"0","signUp":"0","nickname":"薇诺娜·瑞德","privateMessagePointWeb":"0","privateMessagePoint":"0","isClaim":"0","companyName":"信联资信服务有限公司北京分公司","isExpired":"0","pleaseAnswerCount":"1","vnum":"0","bizCardUnread":"0","mobile":"13375358581"}'
r = parse.quote(s)
print(parse.quote(r))



session.cookies.update(cookiejar_from_dict({
    '_ga': 'GA1.2.631538566.1562633250',
    '_gid': 'GA1.2.286054604.1562633250',
    '_gat_gtag_UA_123487620_1': '1',
    'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1562633112',
    'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1562633250',
    'tyc-user-info': parse.quote(r)
}))






aa = session.post('https://www.tianyancha.com/cd/login.json')
print(session.cookies)
aa.encoding = 'UTF-8'
print(aa.text)