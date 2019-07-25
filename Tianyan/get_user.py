import json
import re
import requests
import time


class GetUserMobile(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.token = self.login()

    def login(self):
        params = {
            'action': 'login',
            'username': self.username,
            'password': self.password
        }
        resp = self.download('http://api.fxhyd.cn/UserInterface.aspx', params=params)
        token = resp.text.split('|')[-1]
        return token

    def download(self, url, params=None, data=None):
        return self.session.get(url, params=params, data=data)

    def get_mobile(self):
        params = {
            'action': 'getmobile',
            'token': self.token,
            'itemid': '7344',
            'timestamp': 'TIMESTAMP'

        }
        url = 'http://api.fxhyd.cn/UserInterface.aspx'
        resp = self.download(url, params=params)
        mobile = resp.text.split('|')[-1]
        print(mobile)
        return mobile

    def get_sms_code(self, mobile):
        params = {
            'action': 'getsms',
            'token': self.token,
            'itemid': '7344',
            'mobile': mobile,
            'release': '1',
            'timestamp': 'TIMESTAMP'
        }
        url = 'http://api.fxhyd.cn/UserInterface.aspx'
        num = 0
        while True:
            if num == 20:
                return 0
            resp = self.download(url, params=params)
            resp.encoding = 'UTF-8'
            if resp.text != '3001' and resp.text != '2005':
                code = re.findall(r'\d{4}', resp.text, re.S)
                sms_verify_code = code[0] if code else ''
                return sms_verify_code
            else:
                print(f'第{num}次获取')
            time.sleep(1)
            num += 1


    def run(self):
        mobile = self.get_mobile()
        sms_code = self.get_sms_code(mobile)
        print(sms_code)



if __name__ == '__main__':
    getuser = GetUserMobile('winshell256', '123123123')
    getuser.run()
