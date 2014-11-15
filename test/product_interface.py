#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-10-29"
import zlib, base64
import requests

file_name = '1.jpg'
with open(file_name,'rb') as f:
    zdata = zlib.compress(f.read())
    basedata = base64.b64encode(zdata)
data = {
    'barcode': '1234563214569',
    'product': {
        'goods': {
            'name': '老谭',
            'guide_price': '3.5',
            'introduce': '酸菜面',
            'detail_info': {'净重':'500g'},
            'pack_list': {'方便面':'2包'}
        },
        'company': {
            'name': '万网01',
            'address': '南四街4号',
            'website': 'www.net.cn',
            'service_phone': '123456456463'

        },
        'services':[

            {
                'phone_num': '0210-444',
                'address': '黄中立'
            },
            {
                'phone_num': '010-444',
                'address': '黄中华'
            }
        ],
        'images':[
            {
                'desc': 'no zuo,no die',
                'file_name': file_name,
                'file_data': basedata

            }
        ]

    }
}
import json
json_data = json.dumps(data)
# print json_data
rsp =requests.post('http://127.0.0.1:8080/api/product',data=json_data)
print rsp
dict_data = json.loads(rsp.text)
print dict_data