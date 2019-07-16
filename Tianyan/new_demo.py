import os
import requests
import json
from requests.sessions import cookiejar_from_dict
from datetime import datetime
import execjs
import cmd



#
# with open('geetest.js', 'r') as f:
#     result = execjs.compile(f.read())

p = os.popen('node geetest.js')
s = p.readlines()

print(s)

