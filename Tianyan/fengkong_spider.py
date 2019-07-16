import json
import logging
import requests
from lxml import etree

logger = logging.getLogger('fengkong')


class RiskInfo(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        # 获取vip cookie
        self.cookies = self._get_cookies()

    @staticmethod
    def _get_redis():
        """
        获取redis数据库中cookie
        :return:
        """
        pass

    @staticmethod
    def _get_cookies() -> dict:
        """
        获取cookies， 可优化，待修改
        :return:
        """
        with open('cookies.txt', 'r') as f:
            cooks = json.load(f)

        cookies = {}
        for coo in cooks:
            name = coo['name']
            value = coo['value']
            cookies[name] = value

        return cookies

    def download(self, url: str):
        """
        下载器
        :param url:
        :return:
        """
        # 没返回text
        return requests.get(url, headers=self.headers, cookies=self.cookies)

    def get_xpath(self, xpath: str, response=None, html=None):
        """
        解析
        :param response:
        :return:
        """
        data = None
        if response:
            data_code = etree.HTML(response)
            data = data_code.xpath(xpath)

        if html is not None:
            data = html.xpath(xpath)

        return data

    def get_url_detail(self, url: str):
        # 下载当天监控的最新企业消息
        response = self.download(url)
        # 获取url，当天企业的详情页
        info= self.get_xpath('//div[@class="watch-card"][1]//div[@class="section"]//a[@class="link-click"]/@href', response=response.text)
        today = self.get_xpath('//div[@class="watch-card"][1]/div[@class="header"]/div[@class="date"]/text()', response=response.text)
        today = today[0] if today else ''
        if today != '今天':
            print('今日监控动态为空')
            return

        if not info:
            print('今日无监控动态')
            return

        return info

    def get_company_data(self, titles, tday, t_falv, warnings):
        """
        获取公司的详情数据
        :param titles: 数据的title
        :param tday: 总共有几条监控动态
        :param t_falv: 公司监控动态名称
        :return:
        """
        gonsi_list = []
        # 对每个titles列表（可能有多个动态名称，title不一样）每个tday（每个公司的动态，法律诉讼，专利等数据），t_falv(公司动态的名称)
        for title, table, falv, warning in zip(titles, tday, t_falv, warnings):
            falv_dic = {}
            falv_list = []
            # 循环每一个tbody， 下面有很多tr数据
            for trs in self.get_xpath('./tr', html=table): #原始xpath    table.xpath('./tr')
                info = {}
                # 对每一个td，进行取值，并且枚举出index，与title匹配
                for num, td in enumerate(self.get_xpath('./td', html=trs)): # 原始xpath    trs.xpath('./td')
                    # 规则 一个tr下的每一条td进行枚举，匹配他的title
                    info[title[num]] = self.get_xpath('.//text()', html=td)[0] if self.get_xpath('.//text()', html=td) else '' # 原始xpath    td.xpath('.//text()')

                falv_list.append(info)
            # 将每个动态构建成一个列表数据
            falv_dic[falv] = falv_list
            # 警示信息
            falv_dic['标签'] = warning
            # 每个公司做成一个大数据，包含所有动态
            gonsi_list.append(falv_dic)

        return gonsi_list

    def origin_data(self, info):
        """
        获取公司原始数据
        :return:
        """
        data_info_list = []
        for url in info:
            print(url)
            data = {}  # 公司数据
            resp2 = self.download(url)
            data_code = etree.HTML(resp2.text)
            gongsiming = self.get_xpath('//div[@class="header"]/a/text()', html=data_code) # 公司名称
            gongsiming = gongsiming[0] if gongsiming else ''

            title = self.get_xpath('//div[@id="_container_watchDetailPage"]/div[1]//table/thead', html=data_code)  # 获取thead

            titles = [i.xpath('./tr//text()') for i in title]  # titles就是所有公司诉讼专利等title
            tday = self.get_xpath('//div[@id="_container_watchDetailPage"]/div[1]//table/tbody', html=data_code)  # 获取每个公司的tbody  也就是诉讼，专利等
            # 获取单个公司的动态名称，如法律诉讼，专利信息等
            t_falv = self.get_xpath('//div[@id="_container_watchDetailPage"]/div[1]//div[@class="watch-timeline"]//div[@class="intro"]/span[1]/text()', html=data_code)
            warnings = self.get_xpath('//div[@id="_container_watchDetailPage"]/div[1]//div[@class="watch-timeline"]//div[@class="intro"]/span[2]/text()', html=data_code)

            gonsi_list = self.get_company_data(titles, tday, t_falv, warnings)  # 获取公司详情数据
            data[gongsiming] = gonsi_list  # 拼接成公司的一个公司一个数据
            print(data)
            data_info_list.append(data)

        # 拼接成一个总的用户监控数据
        return {
            'result': data_info_list
        }

    def save_txt(self, result, file_name):
        """
        保存文件
        :param result:
        :return:
        """
        with open(f'{file_name}.txt', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(result))

    def run(self, url):
        """
        控制
        :param url:
        :return:
        """
        # 获取今日详情页中的监控动态
        info = self.get_url_detail(url)
        if not info:
            print('********数据为空*********')
            return
        result = self.origin_data(info)
        self.save_txt(result, 'data_info_list')

    def get_news_company_list(self, company_id_list):
        """
        获取指定企业id的数据
        :param company_id_list: 企业id列表
        :return:
        """
        company_list = [
            f'https://www.tianyancha.com/usercenter/watch/detail?watchType=1&gid={num}&extraId=&reportType=0' for num in company_id_list
        ]
        result = self.origin_data(company_list)
        self.save_txt(result, 'news_company_list')


if __name__ == '__main__':
    url = 'https://www.tianyancha.com/usercenter/watch'
    risk = RiskInfo()
    risk.run(url)
    # li = ['9519792']
    # risk.get_news_company_list(li)