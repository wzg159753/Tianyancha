import json
import re
import base64
from io import BytesIO
from datetime import datetime

import requests
from PIL import Image
from lxml import etree
from requests.sessions import cookiejar_from_dict


class Send_Click(object):
    """
    点触验证码
    """

    def __init__(self):
        cookies = self._get_cookies()
        self.session = requests.Session()
        self.session.cookies = cookiejar_from_dict(cookies)  # session设置cookie

    @staticmethod
    def _get_cookies():
        """
        获取cookie 拼接cookie
        :return:
        """
        cookie = {}
        with open('cookies.txt', 'r') as f:
            result = json.load(f)

        for c in result:
            name = c.get('name')
            value = c.get('value')
            cookie[name] = value

        return cookie

    def get_xpath(self, response, xpath, html=None):
        """
        解析器
        :param response:
        :param xpath:
        :param html:
        :return:
        """
        if html is None:
            html = etree.HTML(response)
            return html.xpath(xpath)
        else:
            return response.xpath(xpath)

    def download(self, url, params=None):
        """
        下载器
        :param url:
        :param params:
        :return:
        """
        return self.session.get(url, params=params)

    def verify(self, response):
        """
        验证是不是点触验证码
        :param response:
        :return:
        """
        title = re.search(f'<title>(.*?)</title>', response)
        return title.group(1) if title else None

    def slice(self, targetImage, bgImage):
        """
        拼接图片验证码
        :param targetImage: 验证图片 点击顺序字符
        :param bgImage: 验证图片  字符
        :return:
        """
        # 打开文件二进制流图片bytes数据
        img = Image.open(BytesIO(base64.urlsafe_b64decode(targetImage)))
        img2 = Image.open(BytesIO(base64.urlsafe_b64decode(bgImage)))

        # new_image 是拼接好的图片
        new_image = Image.new('RGB', (320, 130), 'red')
        new_image.paste(img, (0, 0))
        new_image.paste(img2, (0, 30))

        new_image.show()

        # ===============模拟打码平台=================
        lis = []
        for _ in range(4):
            x = int(input('请输入坐标x:'))
            if x == 0:
                break
            y = int(input('请输入坐标y:'))
            lis.append({'x': x, 'y': y})

        return lis
        # 返回坐标列表

    def verify_image(self):
        # 获取图片验证码返回的图片  b64串
        url = f"http://antirobot.tianyancha.com/captcha/getCaptcha.json?t={str(int(datetime.now().timestamp() * 1000))}"
        result = self.download(url)  # 获取数据
        data = result.json().get('data')
        targetImage = data.get('targetImage')  # 拿到要顺序点击的字符
        bgImage = data.get('bgImage')  # 拿到字符图片
        captchaId = data.get('id')  # 拿到图片id

        # 拼接图片  函数里面接入打码平台
        lis = self.slice(targetImage, bgImage)

        # 拼接参数  发送验证请求
        params = {
            'captchaId': captchaId,  # 图片唯一id
            'clickLocs': json.dumps(lis),  # 图片坐标
            't': str(int(datetime.now().timestamp() * 1000))  # 当前时间戳
        }
        # 验证成功
        resp = self.download("http://antirobot.tianyancha.com/captcha/checkCaptcha.json", params=params)
        # print(resp.json().get('state'))
        return resp.json().get('state')

    def run(self, url):
        # 爬接口  如果是正常网页  title不会是  天眼查验证
        resp = self.download(url)
        # print(resp.text)
        title = self.verify(resp.text)
        print(title)
        if title != '天眼查校验':
            # 如果不是点触验证码，就可以调用自己的接口  爬爬爬
            result = self.get_xpath(response=resp.text, xpath='//div[@class="result-list sv-search-container"]/div')
            # print(result)
            # 继续操作
        else:
            # 如果是点触验证码
            # 调用验证 接打码平台 返回坐标 [{"x":72,"y":66},{"x":97,"y":32}]  坐标类型list 里面每个字符组成一个字典x,y  依次顺序
            if self.verify_image() == 'ok':
                # 可以继续爬这个接口  url
                # result = self.download(url) # 验证成功后可以继续操作
                # print(result.text)
                pass
            else:
                # 没验证成功  继续验证
                resp = self.verify_image()
                print(resp)


if __name__ == '__main__':
    click = Send_Click()
    # 爬一个接口
    click.run('https://www.tianyancha.com/company/3270966165')
