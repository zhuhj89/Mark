#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-10-31"

import requests
import json
url = 'http://127.0.0.1:8080/api/audit'
# params = {
#     'agent_name': 'wanwang',
#     'password': '123456',
#     'domain_name': ['1234567890123.niot.cn','1234567890155.niot.cn']}
#
# r = requests.get(url, params=params)
# print r.url
# print r.text
# print type(r.text)
# data = json.loads(r.text)
# print data['result']['reason']




import zlib, base64
import requests

file_name = '212.jpg'
with open(file_name, 'rb') as f:
    zdata = zlib.compress(f.read())
    basedata = base64.b64encode(zdata)
data = {

    "agent_info": {
        "agent_name": 'wanwang',
        "passwd": '123456'
    },
    "audit_data": {
        "bar_code": "6921734900241",
        "bar_code_image": {
            "file_name": file_name,
            "file_data": basedata,

        },
        'biz_lic_image':{}


    }

}
rp = requests.post(url,data=json.dumps(data))
print rp.text