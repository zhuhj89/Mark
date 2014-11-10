#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-10-14"

from suds.client import Client
from util.db_connection import epp_ms_session as db_mark
import base64
import json
import zlib
# url = 'http://183.63.152.236:8000/soap/productService?wsdl'
# url = 'http://127.0.0.1:8080/soap/productService?wsdl'
# client = Client(url)
# result = client.service.get_product_info('6959764600336')
# #
# print result
# rsp_dict = json.loads(result)
# print rsp_dict['product']['goods']
# detail_info = rsp_dict['product']['goods']['detail_info']
# print detail_info
# detail_dict = json.loads(detail_info)
# print type(detail_dict)
# for key, values in detail_dict.items():
#     print key,values

# # print type(rsp_dict)
# print rsp_dict['code']
# print rsp_dict['msg']
# print rsp_dict['product']['services']
# print rsp_dict['product']['company']
# print rsp_dict['product']['goods']
# images = rsp_dict['product']['images']
# for image in images:
#     with open(image['file_name'],'wb') as f:
#         b64data = base64.b64decode(image['file_data'])
#         zdata = zlib.decompress(b64data)
#         f.write(zdata)
#         f.close()
#     print image['desc']

#
from app.models.product_info import ProductInfo
from app import db
product = ProductInfo.query.filter(ProductInfo.product_code == '1234563214569').first()

detail_info = json.loads(product.detail_info)
print detail_info
for key, value in detail_info.items():
    print key, value

# print product.detail_info
# detail_info = {}
# detail_info['颜色'] = '红色'
# detail_info['容量'] = '600ml'
#
# detail_json = json.dumps(detail_info)
#
# product.detail_info = detail_json
#
# db.session.commit()

# print details,type(details)
# detail_dict = json.loads(details)
# for key, values in detail_dict.items():
#     print key,values



