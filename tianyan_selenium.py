import json
import requests
from lxml import etree


with open('cookies.txt', 'r') as f:
    cooks = json.load(f)

cookies = {}
for coo in cooks:
    name = coo['name']
    value = coo['value']
    cookies[name] = value
# 获取vip的cookies，拼接成常规cookies


resp = requests.get('https://www.tianyancha.com/usercenter/watch', cookies=cookies)
html = etree.HTML(resp.text)
# 获取当日监控公司的当天的监控信息，抽取出当天的url
info = html.xpath('//div[@class="watch-card"][1]//div[@class="section"]//a[@class="link-click"]/@href')
print(info)


f = open('data.txt', 'w', encoding='UTF-8')

for url in info:

    data = {} # 公司数据

    resp2 = requests.get(url, cookies=cookies)
    data_code = etree.HTML(resp2.text)
    # print(resp2.text)
    # 老办法  有数据不全
    gongsiming = data_code.xpath('//div[@class="header"]/a/text()')[0] # 公司名称

    title = data_code.xpath('//div[@id="_container_watchDetailPage"]/div[1]//table/thead') # 获取thead
    titles = [i.xpath('./tr//text()') for i in title] # titles就是所有公司诉讼专利等title
    tday = data_code.xpath('//div[@id="_container_watchDetailPage"]/div[1]//table/tbody') # 获取每个公司的tbody  也就是诉讼，专利等
    t_falv = data_code.xpath('//div[@id="_container_watchDetailPage"]/div[1]//div[@class="watch-timeline"]//div[@class="intro"]/span[1]/text()')
    # print(t_falv)
    # tds = [i.xpath('./tr') for i in tday] #

    # 每一个公司有一个或多个诉讼或专利

    # 循环出每一个维度
    gonsi_list = []

    for title, table, falv in zip(titles, tday, t_falv):
        # 循环每一个tr
        falv_dic = {}
        falv_list = []
        for trs in table.xpath('./tr'):
            info = {}
            # 对每一个td，进行取值，并且枚举出index，与title匹配
            for num, td in enumerate(trs.xpath('./td')):
                info[title[num]] = td.xpath('.//text()')[0]

            falv_list.append(info)
        falv_dic[falv] = falv_list
        gonsi_list.append(falv_dic)

            # f.write(str(info) + '\n')
    data[gongsiming] = gonsi_list
    f.write(str(data) + '\n')

f.close()


