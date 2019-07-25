import json
import re
import random
import time

import redis
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Tianyan.get_user import GetUserMobile
from xlsxwriter import Workbook


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
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 0.5, 0, 0.5, 0, 0, -1, -1, -0.5, -1, -1, -0.5, -1, -0.5, -0.5, -1, -1, -0.5, -1, 0.4, 0.4, 0, 0, 0.4, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1])
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
        track = list()
        length = distance - 6
        x = random.randint(1, 5)
        while length - x > 4:
            track.append([x, 0, 0])
            length = length - x
            x = random.randint(1, 15)

        for i in range(length):
            if distance > 47:
                track.append([1, 0, random.randint(10, 12) / 100.0])
            else:
                track.append([1, 0, random.randint(13, 14) / 100.0])
        return track


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


    def save_redis(self, cookie):
        """
        保存到redis 入队
        :param cookie:
        :return:
        """
        connect = redis.Redis(db=1, host='192.168.0.110', port=6379)
        vip_cookie = cookie
        connect.lpush('cookies', vip_cookie)

    def run(self, *args, **kwargs):
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

# ==================================================注册功能=====================================================
    def register(self, mobile):
        try:
            self.browser.get('https://www.tianyancha.com/')

            login = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="tyc-nav "]/div[@class="nav-item -home"]/a')))
            login.click()

            resiter = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="modulein modulein2 message_box  f-base collapse in"]/div[@class=" login-bottom"]/div')))
            resiter.click()

            input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//input[@class="input contactphone"]')))
            input.send_keys(mobile)

            time.sleep(0.4)
            btn = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="input-group-btn btn -lg btn-primary"]')))
            time.sleep(0.5)
            btn.click()

            time.sleep(1)

        except:
            print('注册错误')
            time.sleep(5)
            self.run_reg()

    def click_register(self, sms_code, mobile):
        sms_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@class="input contactscode"]')))
        sms_input.send_keys(sms_code)

        time.sleep(1)
        password = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="login-word"]/input[@class="input contactword"]')))
        password.send_keys('asdf1123')

        time.sleep(0.5)
        register_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="btn -hg btn-primary -block"]')))
        register_input.click()

        nogap_image, gap_image = self.get_captcha()
        # 对比两张图片的像素点 找出位移
        distance = self.get_gap_offset(nogap_image, gap_image)
        # print(distance)
        tracks = self.get_tracks(distance)
        time.sleep(1)
        self.slide_button(tracks)

        user = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="title link-white"]')))
        if user:
            print('注册成功')
            with open('../mobile3.txt', 'a+') as f:
                f.write(f'mobile: {mobile}, password: asdf1123' + '\n')
            self.browser.delete_all_cookies()
            time.sleep(1)

        else:
            time.sleep(2)
            nogap_image, gap_image = self.get_captcha()
            # 对比两张图片的像素点 找出位移
            distance = self.get_gap_offset(nogap_image, gap_image)
            # print(distance)
            tracks = self.get_tracks(distance)
            time.sleep(1)
            self.slide_button(tracks)
            time.sleep(1)
            self.browser.delete_all_cookies()
            print('注册失败')

        time.sleep(1)




    def run_reg(self):
        get_user = GetUserMobile('winshell256', '123123123')

        while True:
            time.sleep(1)
            mobile = get_user.get_mobile()
            if mobile == '2005':
                time.sleep(20)
                self.run_reg()
            try:
                # 登录
                # time.sleep(1)
                self.register(mobile)
                # 获取两张验证码图片
                nogap_image, gap_image = self.get_captcha()
                # 对比两张图片的像素点 找出位移
                distance = self.get_gap_offset(nogap_image, gap_image)
                # print(distance)
                tracks = self.get_tracks(distance)
                self.slide_button(tracks)

                # time.sleep(2)
                # hidden = self.wait.until(
                #     EC.presence_of_element_located((By.XPATH, '//div[@class="gt_holder gt_popup gt_show"]')))
                # if hidden:
                #     self.run_reg()

                sms_code = get_user.get_sms_code(mobile)
                if sms_code == 0:
                    self.run_reg()
                else:
                    self.click_register(sms_code, mobile)

            except:
                print('error')


def sheet2_w(sample_date):
    ws = Workbook('mobile.xlsx') # 打开一个Excel表格
    wb = ws.add_worksheet('Sheet3') # 添加一个sheet
    # ws.add_worksheet('Sheet1') # 选中一个

    # 构造表格属性
    STYLE_HEADER = {'font_size': 9, 'border': 1, 'bold': 1, 'bg_color': '#B4C6E7', 'align': 'center', 'valign': 'vcenter'}
    STYLE_TEXT = {'font_size': 9, 'border': 1}
    STYLE_NUMBER = {'font_size': 9, 'border': 1, 'num_format': '0.00'}

    # 设置表格属性
    style_header = ws.add_format(STYLE_HEADER)
    style_text = ws.add_format(STYLE_TEXT)
    style_number = ws.add_format(STYLE_NUMBER)

    # 添加表头
    header = ["mobile", "password"]
    # 在第一行设置表头
    wb.write_row('A1', header, style_header)

    # 宽度
    widths = [15, 15]
    # 设置宽度
    for ind, wid in enumerate(widths):
        # print(ind, wid)
        wb.set_column(ind, ind, wid)

    #
    for ind, data in enumerate(sample_date):
        # ind+1 表示第几行， 第二个参数是第几列， 第三个参数是值， 第四个参数是属性
        wb.write(ind + 1, 0, data[0], style_text)
        wb.write(ind + 1, 1, data[1], style_number)

    # 添加完成就关闭
    ws.close()



if __name__ == '__main__':
    tianyan = TianYanCha(username='13853275090', password='wzg159753')
    tianyan.run()
    # tianyan.run_reg()
    # with open('mobile.txt', 'r') as f:
    #     for i in range(200):
    #         print(f.readline())