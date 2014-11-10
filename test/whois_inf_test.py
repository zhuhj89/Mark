
#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-10-30"


import requests
import json
url = 'http://127.0.0.1:8080/api/whois'
r = requests.get(url, params={'domain_name':'1234567890123.niot.cn'})
print r.url
print r.text
data = json.loads(r.text)
print data['data']['registrant']

