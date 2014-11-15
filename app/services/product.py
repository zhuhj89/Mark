#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-10-29"

from flask.ext.restful import Resource
from flask import Flask, request
from app.models import CompanyInfo,ProductInfo,CustomServiceInfo,FileInfo
from util.file_util import remove_file, base64_zip_filedata_to_save
from app.extensions import db
from sqlalchemy import and_
from conf import config
import json
import uuid
import requests
import datetime
class Product(Resource):
    def get(self):
        # return {'hello': 'world'}
        return {'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    def post(self):
        """
          post_data  = {
            'barcode': fields.String,
            'product':
                {
                    'goods': fields.Nested(
                        {
                            'name': fields.String,
                            'guide_price': fields.String,
                            'introduct': fields.String,
                            'detail_info': fields.String,
                            'pack_list': fields.String
                        },
                    'images':
                        {
                            'desc': fields.String,
                            'file_name': fields.String,
                            'file_data': fields.String
                        },
                    'services':[
                        {
                            'phone_num': fields.String,
                            'address': fields.String
                        }
                    ],
                    'company':
                        {
                            'name': fields.String,
                            'service_phone': fields.String,
                            'address': fields.String,
                            'website': fields.String
                        }
                }
        }
        :return:
        """

        try:
            req = request.get_json(force=True)
            print 'type(req)>>>',type(req)
            response = {
                'code': '200',
                'msg': 'upload ok!!!',
                'result': {}
            }
            barcode = req['barcode']
            product = req['product']
            if product:
                goods = None
                services = None
                company = None
                images = None
                if 'goods' in product:
                    goods = product['goods']
                if 'services' in product:
                    services = product['services']
                if 'company' in product:
                    company = product['company']
                if 'images' in product:
                    images = product['images']
                if goods:
                    product_s = ProductInfo.query.filter(ProductInfo.product_code == barcode).first()
                    if not product_s:
                        product_info = ProductInfo()
                    else:
                        product_info = product_s
                    product_info.product_code = barcode
                    product_info.name = goods['name']
                    product_info.introduce = goods['introduce']
                    product_info.guide_price = goods['guide_price']
                    product_info.detail_info = json.dumps(goods['detail_info'])
                    product_info.pack_list = json.dumps(goods['pack_list'])
                    if company:
                        if not product_info.company:
                            product_info.company = CompanyInfo()
                        product_info.company.name = company['name']
                        product_info.company.address = company['address']
                        product_info.company.service_phone = company['service_phone']
                        product_info.company.website = company['website']

                    if services:
                        if product_info.services:
                            CustomServiceInfo.query.filter(CustomServiceInfo.product_id == product_info.id).delete()
                        product_info.services = []
                        for service in services:
                            ser = CustomServiceInfo()
                            ser.phone_num = service['phone_num']
                            ser.address = service['address']
                            product_info.services.append(ser)
                    if product_s:
                        db.session.add(product_info)
                        db.session.flush()
                    if images:
                        query = FileInfo.query.filter(and_(FileInfo.category == '01',
                                                           FileInfo.ref_id == product_info.id))
                        image_list = query.all()
                        print image_list
                        if image_list:
                            for image in image_list:
                                file_path = image.file_path
                                remove_file(file_path)
                                query.delete()

                        for image in images:
                            f_info = FileInfo()
                            f_info.category = '01'
                            f_info.ref_id = product_info.id
                            f_info.desc = image['desc']

                            file_name = image['file_name']
                            filename = str(uuid.uuid4()) + file_name[file_name.rfind('.'):]
                            file_data = image['file_data']
                            result =base64_zip_filedata_to_save(filename, file_data, '02')
                            if result[0] == 1:
                                save_path = result[1]
                                f_info.file_path = save_path
                            db.session.add(f_info)
                db.session.merge(product_info)
                db.session.commit()
                url = config.__PRODUCT_POST_URL__
                data= {}
                data['products'] = json.dumps(req)
                rsp = post_to_app(url, data)
                print "rsp >>>",rsp
                if rsp['status'] == '0':
                    response['result']['url'] = rsp['url']
                elif rsp['status'] == '9':
                    response['code'] = '201'
                    response['msg'] = 'upload failed!'
        except Exception, e:
            response['code'] = '202'
            response['msg'] = e
        print "response >>", type(response), response
        return response

def post_to_app(url,data):
    import urllib
    rsp = requests.post(url, urllib.urlencode(data))
    print rsp
    result = json.loads(rsp.text)
    return result
