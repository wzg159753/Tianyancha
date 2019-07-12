from datetime import datetime
import json
import requests
from requests.sessions import cookiejar_from_dict


session = requests.Session()

def download(url):
    return session.get(url)


if __name__ == '__main__':
    url = 'https://www.tianyancha.com/'
    resp = download(url)
    resp.encoding = 'UTF-8'

    url1 = f'https://www.tianyancha.com/claim/getLabels.json?_={int(datetime.now().timestamp() * 1000)}'
    resp1 = session.get(url1)
    print(resp1.text)
    # uri = f'https://www.tianyancha.com/user/getHomeNavHeader.html?_={int(datetime.now().timestamp() * 1000)}'
    # resp2 = session.get(uri)
    cookie = {
        'bannerFlag': 'undefined'
    }
    cookies = cookiejar_from_dict(cookie)
    session.cookies.update(cookies)
    resp3 = session.get('https://www.baidu.com')
    print(resp3)

