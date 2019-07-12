import json
from datetime import datetime
import requests
from lxml import etree

#
# headers = {
#     'Content-Type': 'application/json; charset=UTF-8',
# }
#
# data = {
#     'uuid': int(datetime.now().timestamp() * 1000)
# }
#
# url = 'https://www.tianyancha.com/verify/geetest.xhtml'
#
# resp = requests.post(url, headers=headers, data=json.dumps(data))
# resp.encoding = 'UTF-8'
# print(resp.json())
li = [
    'aliyungf_tc=AQAAAMqqs3ftsgUA+CzCG01fOUWFA7N0; ssuid=4319276542; bannerFlag=undefined; csrfToken=PbNmCWzEwwjNGJWsgDj1he5z; TYCID=4f9440309d6e11e9bd198f61c0647ff5; undefined=4f9440309d6e11e9bd198f61c0647ff5; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1562143272; _ga=GA1.2.792707609.1562143273; _gid=GA1.2.2060112714.1562143273; token=1cd0b3768a5d4d82be57866708f2d402; _utm=75ad5dcda62d45d09248e2e94950790b; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E9%2583%25AD%25E9%259A%2597%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252247%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzYxNjI3Mzg1NyIsImlhdCI6MTU2MjE0MzY2NSwiZXhwIjoxNTkzNjc5NjY1fQ.-wfbquQre-c_hv3799su55BHg2-_R5ITmEYtZ1ee4EU6RUbes1Bp4KVVcW4Q7G2bNhp9PF0AFbG2DNlO6-2glg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217616273857%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzYxNjI3Mzg1NyIsImlhdCI6MTU2MjE0MzY2NSwiZXhwIjoxNTkzNjc5NjY1fQ.-wfbquQre-c_hv3799su55BHg2-_R5ITmEYtZ1ee4EU6RUbes1Bp4KVVcW4Q7G2bNhp9PF0AFbG2DNlO6-2glg; RTYCID=aee0fe2548404fcc90a861726c061e24; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1562144471; CT_TYCID=37fb163a720d4cc685eea0ea7aa75ebf; cloud_token=c539cfa8d7734ae18df58ccb2b1a3622; cloud_utm=fe073ada53d24cd18a76c89f2881ad59',
    'aliyungf_tc=AQAAALbPHXXLvwkA+CzCG6MY6KaVJnaf; csrfToken=ljP0i10UttrSTUg9ABv-37W4; TYCID=bc7d96909d5c11e9a75059cd4b429afd; undefined=bc7d96909d5c11e9a75059cd4b429afd; ssuid=7874570525; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1562135724; _ga=GA1.2.1320141454.1562135724; _gid=GA1.2.1949420684.1562135724; token=8c7b2e403b994eb58e8dc9fc67b59531; _utm=880e51adcf45449cb48c27c3f4bb0a08; RTYCID=6b040845019845e4b7e8966c7852c19a; CT_TYCID=86c57cc21887453f981283a02822c250; bannerFlag=true; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E9%2583%25AD%25E9%259A%2597%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252247%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzYxNjI3Mzg1NyIsImlhdCI6MTU2MjEzNzM5NSwiZXhwIjoxNTkzNjczMzk1fQ.lnAvLLGGu90jJsuul8ODC2FE7E5gW5hk3nZ0TnLtze7Ng-65qf9DGKJrb5e04GCBEAGm5MFzK2X-uwjvj2kThg%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217616273857%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzYxNjI3Mzg1NyIsImlhdCI6MTU2MjEzNzM5NSwiZXhwIjoxNTkzNjczMzk1fQ.lnAvLLGGu90jJsuul8ODC2FE7E5gW5hk3nZ0TnLtze7Ng-65qf9DGKJrb5e04GCBEAGm5MFzK2X-uwjvj2kThg; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1562137473; cloud_token=82fb4279158a4b42ae47416bd57970e4; cloud_utm=801dbd452b2b41e58dd9ec961d8d594d'
]


session = requests.Session()
session.headers = {

    'Host': 'www.tianyancha.com',
    # 'Referer': 'https://www.tianyancha.com/login?from=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%3Fbase%3Dtj',
    # 'Upgrade-Insecure-Requests': '1',
    'Cookie': li[0],
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


resp = session.get('https://www.tianyancha.com/')

html = etree.HTML(resp.text)
response = html.xpath('//div[@class="row"]/div[@class="col-11"]/a/@href | //div[@class="row"]/div[@class="item -right -prov"]/a/@href')
n = 0
for i in response:
    r1 = session.get(i)
    code = etree.HTML(r1.text)
    default_url = code.xpath('//div[@class="content"]/div[@class="header"]/a/@href')
    for j in default_url:
        if n > 90:
            session.headers['Cookie'] = li[1]
            n = 0
        info = session.get(j)
        gongsi = etree.HTML(info.text)
        table = gongsi.xpath('//table[@class="table -striped-col -border-top-none -breakall"]/tbody/tr')
        n += 1
        for i in table:
            # data = {
            #     i.xpath('./td[1]/text()')[0]: i.xpath('./td[2]/text()')[0],
            #     i.xpath('./td[3]/text()')[0]: i.xpath('./td[4]/text()')[0]
            # }
            # print(data)
            print(i.xpath('./td[1]/text()')[0])
            print(i.xpath('./td[2]/text() | ./td[2]/div/text()'))
            print(i.xpath('./td[3]/text()'))
            print(i.xpath('./td[4]/text() | ./td[2]/span/text()'))
        print(n)