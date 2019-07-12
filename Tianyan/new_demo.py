import requests
import json
from requests.sessions import cookiejar_from_dict
from datetime import datetime

session = requests.session()

session.headers = {
    'Host': 'www.tianyancha.com',
    'Connection': 'keep-alive',
    # 'Content-Length': '252',
    # 'Accept': '*/*',
    # 'Origin': 'https://www.tianyancha.com',
    # 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    # 'Content-Type': 'application/json; charset=UTF-8',
    # 'Referer': 'https://www.tianyancha.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    # 'Cookie': 'aliyungf_tc=AQAAAFNYw1nemQoA+CzCGx2PaswJYQ8f; ssuid=8984269572; bannerFlag=undefined; _ga=GA1.2.631538566.1562633250; _gid=GA1.2.286054604.1562633250; _gat_gtag_UA_123487620_1=1; csrfToken=8YyJsLT1RbW5IolHsu10G64E; TYCID=211456e0a1e311e9afdbf1c40a1a2bcb; undefined=211456e0a1e311e9afdbf1c40a1a2bcb; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1562633112; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1562633250'
}

with open('cookies.txt', 'r') as f:
    cooks = json.load(f)

cookies = {
    # 'ssuid': '1230936176',
    # 'aliyungf_tc': 'AQAAABsw+ywkxgkA+CzCG+0nIY4tlvCt',
    # 'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1562726224',
    # 'bannerFlag': 'undefined',
    # '_gid': 'GA1.2.376412601.1562726224',
    # '_ga': 'GA1.2.1141158955.1562726224',
    # 'csrfToken': 'ol7a-Kj3fU3YfqKprfN0lwKP',
    # 'TYCID': '98e85da0a2bb11e999694715b900225f',
    # 'undefined': '98e85da0a2bb11e999694715b900225f',
    # '_gat_gtag_UA_123487620_1': '1',
    # 'tyc-user-info': '%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2585%258B%25E9%2587%258C%25E6%2596%25AF%25E8%2592%2582%25E5%25A8%259C%25C2%25B7%25E8%2589%25BE%25E4%25BC%25AF%25E7%259B%2596%25E7%2589%25B9%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%25221%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzg1MzI3NTA5MCIsImlhdCI6MTU2MjcyNjIzMCwiZXhwIjoxNTk0MjYyMjMwfQ.7UY3yLpC_K0FBwOjaQjLsu8Pt0VYPmtRKELQGepZ5xTtEr6s9WHVJTpv4MnGCLCrsFO2X397O1JMJCkme8F2Qg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213853275090%2522%257D',
    'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzM3NTM1ODU4MSIsImlhdCI6MTU2Mjc0Mzg4MSwiZXhwIjoxNTk0Mjc5ODgxfQ.79x-vx6E15EGpvKzwIGv2QDeez9_yi-VhKvsF71kIL71UdccSadB9PMIYX0oCocsuA7pcsx5_fG0f2OoHvQ2qg',
    # 'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1562726233'
}



session.cookies.update(cookiejar_from_dict(cookies))


# resp = session.post('https://www.tianyancha.com/cd/login.json')
# print(resp.cookies)
print(session.cookies)

resp = session.get('https://www.tianyancha.com/usercenter/modifyInfo')
print(resp.text)
