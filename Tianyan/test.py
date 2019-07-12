import json
import base64
from io import BytesIO
from datetime import datetime


import requests
from PIL import Image
from lxml import etree
from requests.sessions import cookiejar_from_dict


cookie = {}
with open('cookies.txt', 'r') as f:
    result = json.load(f)

for c in result:
    name = c.get('name')
    value = c.get('value')
    cookie[name] = value

session = requests.Session()
session.cookies = cookiejar_from_dict(cookie)

resp = session.get('https://www.tianyancha.com/search?base=bj')
print(resp.text)
html = etree.HTML(resp.text)

url_lists = html.xpath('//div[@class="result-list sv-search-container"]/div')
print(url_lists)


url = f"http://antirobot.tianyancha.com/captcha/getCaptcha.json?t={str(int(datetime.now().timestamp() * 1000))}"

data = session.get(url)
print(data.json())
bgImage = data.json().get('data').get('bgImage')
targetImage = data.json().get('data').get('targetImage')
print(base64.urlsafe_b64decode(bgImage))
print(base64.urlsafe_b64decode(targetImage))
objie = {}
objie['captchaId'] = data.json().get('data').get('id')



# with open('targetImage.png', 'wb') as f:
#     f.write(base64.urlsafe_b64decode(targetImage))
# with open('bgImage.png', 'wb') as f:
#     f.write(base64.urlsafe_b64decode(bgImage))


img = Image.open(BytesIO(base64.urlsafe_b64decode(targetImage)))
img2 = Image.open(BytesIO(base64.urlsafe_b64decode(bgImage)))
print(img.size)
print(img2.size)


new_image = Image.new('RGB', (320, 130), 'red')
new_image.paste(img, (0, 0))
new_image.paste(img2, (0, 30))

new_image.show()
lis = []
for _ in range(4):
    x = int(input('请输入坐标x:'))
    if x == 0:
        break
    y = int(input('请输入坐标y:'))
    lis.append({'x': x, 'y': y})

print(lis)
send_url = "http://antirobot.tianyancha.com/captcha/checkCaptcha.json"
params = {
    'captchaId': data.json().get('data').get('id'),
    'clickLocs': json.dumps(lis),
    't': str(int(datetime.now().timestamp() * 1000))
}

se = session.get(send_url, params=params)
print(se.text)
#
#
dd = session.get('https://www.tianyancha.com/company/3270966165')
print(dd.text)