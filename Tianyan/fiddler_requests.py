import re
import json
from datetime import datetime
from requests.sessions import cookiejar_from_dict
import requests
import execjs

with open('test.js', 'r') as f:
    my_js = execjs.compile(f.read())

ssuid = my_js.call('get_suid')
print(f'ssuid={ssuid}', f'当前13位时间戳={str(int(datetime.now().timestamp() * 1000))}')
session = requests.Session()
headers = {
    'Host': 'www.tianyancha.com',
    'Connection': 'keep-alive',
    'Content-Length': '252',
    'Accept': '*/*',
    'Origin': 'https://www.tianyancha.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Referer': 'https://www.tianyancha.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'

}

session.get('https://www.tianyancha.com/')
session.cookies.update(cookiejar_from_dict({
    'ssuid': '5385309444',
	'bannerFlag': 'undefined',
    'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': str(int(datetime.now().timestamp() * 1000)),
    'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': str(int(datetime.now().timestamp() * 1000))
}))

session.get(f'https://www.tianyancha.com/newest.html?ps=40&_={str(int(datetime.now().timestamp() * 1000))}')
t1 = int(datetime.now().timestamp() * 1000)




session.get(f'https://www.tianyancha.com/tongji/1562724106551.json?_={str(int(datetime.now().timestamp() * 1000))}')




# 第一次请求
# get gt or challage
data = {
    'uuid': my_js.call('get_uuid')
}

header = {
    'Content-Type': 'application/json; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
resp = session.post('https://www.tianyancha.com/verify/geetest.xhtml', data=json.dumps(data), headers=header)
resp.encoding = 'UTF-8'



# 第二次请求
print(resp.json())
data = resp.json().get('data')

info = {
    'gt': data.get('gt'),
    'challenge': data.get('challenge'),
    'product': 'popup',
    'offline': 'false',
    'protocol': 'https://',
    'maze': '/static/js/maze.1.0.1.js',
    'path': '/static/js/geetest.6.0.9.js',
    'pencil': '/static/js/pencil.1.0.3.js',
    'type': 'slide',
    'beeline': '/static/js/beeline.1.0.1.js',
    'voice': '/static/js/voice.1.2.0.js',
    'callback': f'geetest_{str(int(datetime.now().timestamp() * 1000))}'
}

resp = session.get('https://api.geetest.com/get.php', params=info)
challenge = re.search(r'"challenge": "(.*?)",', resp.text).group(1)
print(challenge)
print(resp.text)










# # 第三次请求  参数待解密
# params = {
#     'gt': data.get('gt'),
#     'challenge': challenge,
#     # 加密已经找到  待调试
#     'w': 'ZGtie)qv4qQKPfRU8L46uoDSfZpFOg9BrvMnYFf9B9Qlu8O3dPwWj)1JLkYmBzqYFeb5ojV10dW2X4IDtRNmZLD12fHmQlfuyFAOJhdP70PITYbOHHrTyht874vHlJYPdvzgCScaK)QjzVHJ6R4QtWW0SOz0bUgl(o8tYfImyKpLsVfwxtPfunMoOByU49inbAN3BoVo4dgpwiV3YZjNXlxYObBdw12r)FCv)R0IRxudtxOJxzPvNBEjnJ)4sDKXnpMLVW2TPE(n4sGUVNUfldaxMWZSc)SAqCyF)iEQ)H)mpJNucEwDtvEdo2THaIBdM8JMiw7lDk6)zQHItCrJn0ulKzemHhM4h8g(eItCfZvMoEClxaxxqRwNmEyKLDScUNeEZMqFTfM2iEcaiP20vw..960e3b454bfd2729f954d8e0a01b3c67f20acd8de1a3ef75bfb8c67855558ee6d72e8723ffb317bf38ad4bc6a989811c5987c2cf3b8fe900c1721a91b1e7c18f134665a8669970a55027961644058b706b843d64fa31835c071ee27efb7bac632fa78b3720bc42a2a1ac7d5cc9eef215fb8f165897a4b68c0b02c34acb86f2c8',
#     'callback': f'geetest_{str(int(datetime.now().timestamp() * 1000))}'
# }
#
# result = session.get('https://api.geetest.com/ajax.php', params=params)
#
#
#
#
# # 第四次请求  登录请求  参数是上方返回的参数
# data = {
#     "autoLogin": 'true',
#     "cdpassword": "cf3917ae12e928ce84b71e8fb40e95e0", # 密码加密
#     "challenge": challenge,
#     "loginway": "PL",
#     "mobile": "13853275090", # 手机号
#     "seccode": "113eff3e5059ed3c4956309eb6deeff5|jordan",  # 这两个盐都是上次请求返回的json
#     "validate": "113eff3e5059ed3c4956309eb6deeff5",
# }
#
#
# response = session.post('https://www.tianyancha.com/cd/login.json')
