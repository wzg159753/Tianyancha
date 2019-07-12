import json
import re
import random
import time
import redis
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TianYanCha(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.options = self._set_options()
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.wait = WebDriverWait(self.browser, 10)

    def _set_options(self):
        options = Options()
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--headless")
        return options

    def login(self):
        try:
            self.browser.get('https://www.tianyancha.com/')
            login = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="tyc-nav "]/div[@class="nav-item -home"]/a')))
            login.click()
            time.sleep(0.5)
            click_zhanghao = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@active-tab="1"]')))

            click_zhanghao.click()

            input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="modulein modulein1 mobile_box  f-base collapse in"]/div[@class="pb30 position-rel"]/input')))
            # print(input)

            pwd = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="modulein modulein1 mobile_box  f-base collapse in"]/div[@class="input-warp -block"]/input')))
            input.send_keys(self.username)
            time.sleep(0.5)
            pwd.send_keys(self.password)
            time.sleep(0.5)
            button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="modulein modulein1 mobile_box  f-base collapse in"]//div[@class="btn -hg btn-primary -block"]')))
            time.sleep(0.1)
            button.click()


        except:
            self.browser.quit()

    def get_captcha(self):
        # try:
        # 获取带缺口的图片
        gap_image = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="gt_cut_bg gt_show"]/div')))
        gap_image = self._slice_image(gap_image)

        # 不带缺口的图片
        nogap_image = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="gt_cut_fullbg gt_show"]/div')))
        nogap_image = self._slice_image(nogap_image)

        return (nogap_image, gap_image)

        # except:
        #     print('slice出错')
        #     self.browser.quit()

    def _slice_image(self, image):
        # 用正则获取元素中的图片url
        image_url = re.search(r'url\("(.*?)"\)', image[0].get_attribute('style')).group(1)

        # 获取小图的偏移量  用于拼接
        image_position = [i.get_attribute('style') for i in image]
        # a = [i for i in image_position]
        image_position_list = [re.search(r'background-position: -(.*?)px -?(.*?)px', i).groups() for i in image_position]



        # 访问图片url，获取图片二进制数据
        img = requests.get(image_url).content
        # PIL要从二进制数据读取一个图片的话，需要把他转化为BytesIO
        img = Image.open(BytesIO(img))
        # 生成一个新的大小相同的图片
        new_image = Image.new('RGB', (260, 116))

        # 设置粘贴坐标，坐标每次循环加10， 从左到右依次粘贴
        count_up = 0
        count_low = 0
        # 图片主要分为上下两个部分，所以分成两个循环分别粘贴
        # image_list前26个为上半部分，后26个位下半部分
        # 每个图片大小为10，58
        for i in image_position_list[:26]:
            croped = img.crop((int(i[0]), 58, int(i[0]) + 10, 116))
            new_image.paste(croped, (count_up, 0))
            count_up += 10

        for i in image_position_list[26:]:
            croped = img.crop((int(i[0]), 0, int(i[0]) + 10, 58))
            new_image.paste(croped, (count_low, 58))
            count_low += 10

        return new_image

    # 获取缺口偏移量
    def get_gap_offset(self, nogap_image, gap_image):
        """
        获取缺口偏移量
        :param nogap_image: 不带缺口图片
        :param gap_image: 带缺口图片
        :return:
        """

        # 比较两个像素是否相同
        # 由于是RGB格式，所以需要分别判断每个像素点中的R，G，B值
        def is_pixel_equal(pixel1, pixel2, threshold=50):
            for i in range(3):
                if abs(pixel1[i] - pixel2[i] < threshold):
                    return True
            return False  # 误差过大，表示不相等

        width, height = nogap_image.size
        left = 40
        for i in range(left, width):
            for j in range(height):
                # 获取两张图片相同坐标的像素点进行比较
                nogap_pixel = nogap_image.getpixel((i, j))
                gap_pixle = gap_image.getpixel((i, j))

                # 如果像素不同，返回当前像素的x坐标
                if not is_pixel_equal(nogap_pixel, gap_pixle):
                    left = i
                    return left
        return left

    # 生成滑动轨迹
    # 由于极验的后台在不断的训练识别模型，所以移动轨迹可能是有实效性的，时常需要修改
    # 轨迹要尽量的靠近人类的行为习惯
    def get_tracks(self, distance):
        '''
        来源于物理学中的加速度算距离公式和速度公式： s = vt + 1/2 at^2
                                        v = v_0 + at
        总距离S= 每一次移动的距离之和
        加速度：前3/5S加速度2，后半部分加速度是-3
        '''
        # 初速度
        speed = 0
        # 计算移动距离所需的时间间隔
        t = 0.1
        # 减速阈值（改变加速度的时间点）

        mid = distance * random.randint(1, 4) / random.randint(1, 10)
        # 当前位移
        current = 0
        # 移动轨迹的列表
        move_track_list = []

        while current < distance:
            if current < mid:
                # 加速度为2
                a = 2
                # 距离的计算公式  v0t + 1/2 * a * t^2
                move_distance = speed * t + 0.5 * a * (t ** 2)
                # 将生成的移动距离添加到轨迹列表中
                move_track_list.append(round(move_distance))
                # 当前速度v = v0 + at
                speed += (a * t)
                # 当前位移
                current += move_distance
            else:
                # 当距离大于五分之三的position时，添加减速轨迹，并跳出循环
                move_track_list.extend([3, 3, 2, 2, 1, 1, 0, 0])
                break

        # 识别当前总共移动距离是大于还是小于position
        # 大于则补连续的-1，小于则补连续的1
        offset = sum(move_track_list) - distance
        print(sum(move_track_list), distance)
        print('&'*20, offset)
        if offset > 0:
            print('*'*20, [-3 for i in range(abs(offset))])
            move_track_list.extend([-3 for i in range(offset)])
        elif offset < 0:
            print('=' * 20, [1 for i in range(abs(offset))])
            move_track_list.extend([1 for i in range(abs(offset))])

        # 小幅晃动模拟人在终点附近的左右移动
        move_track_list.extend(
            [1, 1, 1, 1,0, 0.5, 0, 0.5, 0, 0, -1, -1, -0.5, -1, -0.5, -0.5, -1, -1, -0.5, -1, 0.4, 0.4, 0, 0, 0.4, 0.3, 0.1])
        print(move_track_list)
        print(sum(move_track_list))
        return move_track_list

    def get_tracks2(self, distance):

        '''
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+(1/2)at²
        ③v²-v0²=2as

        :param distance: 需要移动的距离
        :return: 存放每0.2秒移动的距离
        '''
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.1
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 4 / 5

        distance += 10  # 先滑过一点，最后再反着滑动回来

        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = 2  # 加速运动
            else:
                a = -3  # 减速运动

            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t

        # 反着滑动到大概准确位置
        for i in range(3):
            tracks.append(-2)
        for i in range(4):
            tracks.append(-1)
        return tracks

    # 滑动
    def slide_button(self, tracks):
        try:
            # 找到滑块位置
            slide_button = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="gt_slider_knob gt_show"]')))
            time.sleep(0.5)
            # 点击拿起滑块
            ActionChains(self.browser).click_and_hold(slide_button).perform()
            time.sleep(1)

            # 根据滑动轨迹，逐步移动鼠标
            for i in tracks:
                ActionChains(self.browser).move_by_offset(xoffset=i, yoffset=0).perform()

            # 松开鼠标
            time.sleep(1)
            ActionChains(self.browser).release().perform()


        except:
            self.browser.quit()



    def __call__(self, *args, **kwargs):
        try:
            # 登录
            self.login()
            # 获取两张验证码图片
            nogap_image, gap_image = self.get_captcha()
            # 对比两张图片的像素点 找出位移
            distance = self.get_gap_offset(nogap_image, gap_image)
            print(distance)
            tracks = self.get_tracks(distance)
            self.slide_button(tracks)
            time.sleep(5)
            # 获取cookies
            cookies = self.browser.get_cookies()
            # 保存到文本
            with open('cookies.txt', 'w') as f:
                json.dump(cookies, f)

            # 保存到redis，json格式， 取出来的时候是一个二进制，先decode再loads
            # self.save_redis(json.dumps(cookies))

            # 测试打印
            for cookie in cookies:
                print({cookie['name']: cookie['value']})

            print('写入成功')
        except:
            self.browser.quit()

    def save_redis(self, cookie):
        """
        保存到redis 入队
        :param cookie:
        :return:
        """
        connect = redis.Redis(db=1, host='192.168.0.110', port=6379)
        vip_cookie = cookie
        connect.lpush('cookies', vip_cookie)


if __name__ == '__main__':
    tianyan = TianYanCha(username='13853275090', password='wzg159753')
    tianyan()