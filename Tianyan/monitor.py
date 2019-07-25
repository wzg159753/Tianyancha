import json
from datetime import datetime

import redis
import execjs
import requests

# connect = redis.Redis(db=1, host='192.168.0.110', port=6379)
#
#
# for i in range(5):
#     vip_cookie = {'ddd': 'ddd', 'aaa': 'aaa'}
#     connect.lpush('cookies', json.dumps(vip_cookie))
#
# result = connect.lrange('cookies', 0, 10)
# print(result)

# ===========================================

# with open('test.js', 'r') as f:
#     result = execjs.compile(f.read())
#
#
#
# rand = result.call('get_rand')
# uid = result.call('get_suid')



# =================== **自动监控 需要企业id** ======================#


class Monitor(object):

    def __init__(self):
        # 初始化headers
        headers = {
            'Access-Control-Request-Headers': 'version,x-auth-token',
            'Access-Control-Request-Method': 'GET',
            # 'Referer': f'https://www.tianyancha.com/company/{company_id}',  # 改企业id
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        # 初始化session
        self.session = requests.Session()
        # 设置持久headers
        self.session.headers = headers
        # 两次请求参数一致
        self.session.params = {
            'type': '1',
            # 'gid': company_id,  # 改企业id 识别企业
            # 'modify': add, # 如果是add就是监控，如果是del就取消监控
            # '_': int(datetime.now().timestamp() * 1000)
        }

    def set_x_auth_token(self) -> None:
        """
        向headers中设置x-auth-token
        :return:
        """
        # 读出cookies
        with open('cookies.txt', 'r') as f:
            cookies = json.load(f)
        # 初始化参数
        cookiess = {
            'version': 'TYC-Web',
            'X-AUTH-TOKEN': ''
        }

        x_auth_token = ''
        for cookie in cookies:
            # 拿到cookie中的auth_token
            if cookie.get('name') == 'auth_token':
                # 将X-AUTH-TOKEN的值设置为cookies中的
                cookiess['X-AUTH-TOKEN'] = cookie.get('value')
                break
        # 更新headers
        self.session.headers.update(cookiess)

    def send_option(self) -> None:
        """
        发送options请求
        :return:
        """
        try:
            self.session.options('https://capi.tianyancha.com/cloud-monitor-provider/v4/monitor/modifyMonitor.json')
        except Exception as e:
            print('options requests error')

    def send_monitor(self) -> None:
        """
        发送监控或取消监控请求
        :return:
        """
        resp3 = self.session.get('https://capi.tianyancha.com/cloud-monitor-provider/v4/monitor/modifyMonitor.json')
        if resp3.status_code == 200:
            print(resp3.status_code)
            print('操作成功')
        else:
            print('操作失败')

    def run_monitor(self, company_id_list: list, status: str) -> None:
        """
        注意顺序，先发送没有x-auth-token的请求
        然后设置x-auth-token到headers
        最后发送监控请求携带x-auth-token
        :return:
        """
        for company_id in company_id_list:
            self.session.headers.update({
                'Referer': f'https://www.tianyancha.com/company/{company_id}',  # 改企业id
            })
            self.session.params.update({
                'gid': company_id,  # 改企业id 识别企业
                'modify': status,  # 如果是add就是监控，如果是del就取消监控
                '_': int(datetime.now().timestamp() * 1000)
            })
            # 第一次请求，一个options请求
            self.send_option()
            # 向headers中设置x-auth-token
            self.set_x_auth_token()
            # 发送监控或取消监控请求
            self.send_monitor()


if __name__ == '__main__':
    monitor = Monitor()
    # 企业id列表
    li = ['22822', '3092687032', '3047175221', '799248041', '1398726953', '22342801']
    monitor.run_monitor(li, 'add')
