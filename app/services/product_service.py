# -*- coding: utf-8 -*-
"""
  the show product Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-21"

from app.extensions import spyne
from flask import url_for
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.model.primitive import Unicode,Integer
from spyne.model.binary import ByteArray
from app.models.product_service_rsp import GetProductResponse,ImageInfo,Company,ProductInfos,CustomService
from app.models.product_service_rsp import AddFileResponse,AddProductResponse,AddCustomServiceResponse,AddCompanyResponse

from util.file_util import save_file,get_file_data,get_image_info
from app.models.company_info import CompanyInfo,add_company_info,get_company_by_company_id
from app.models.custom_service_info import CustomServiceInfo, add_custom_service_info,get_custom_service_by_product_code
from app.models.file_info import FileInfo,add_file,get_file
from app.models.product_info import ProductInfo,add_product_info,get_product_by_id,update_product
import conf.config as config
import uuid
import json
from jinja2 import Template

class ProductService(spyne.Service):
    __service_url_path__ = '/soap/productService'

    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
    # __in_protocol__ = HttpRpc(validator='soft')
    # __out_protocol__ = JsonDocument(ignore_wrappers=True)
    @spyne.srpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, _returns=AddProductResponse)
    def save_product(product_code, name, introduce, detail_info, guide_price, pack_list):
        product = ProductInfo()
        product.product_code = product_code
        product.name = name
        product.introduce = introduce
        product.detail_info = detail_info
        product.guide_price = guide_price
        product.pack_list = pack_list
        pk_id = add_product_info(product)
        rsp = AddProductResponse()
        if pk_id:
            rsp.code = '010'
            rsp.msg = "save Product infomation ok!"
            rsp.p_id = pk_id
            return rsp
        else:
            rsp.code = '011'
            rsp.msg = "save Product infomation failed"
            return rsp


    @spyne.srpc(Unicode, Unicode,Unicode, Unicode, Unicode, _returns=AddCompanyResponse)
    def save_product_company(product_code,name, address,website, service_phone):
        company = CompanyInfo()
        company.name =name
        company.address = address
        company.service_phone = service_phone
        company.website = website
        pk_id = add_company_info(company)
        rsp = AddCompanyResponse()
        if pk_id:
            rsp.code = '020'
            rsp.msg = "Add Product's company infomation ok!"
            rsp.company_id = pk_id
            parm = {'company_id': pk_id}
            update_product(product_code,parm)
            return rsp
        else:
            rsp.code = '021'
            rsp.msg = "Add Product's company infomation failed!"
            return rsp

    @spyne.srpc(Integer, Unicode, Unicode, Unicode,ByteArray(min_occurs=1, nullable=False), _returns=AddFileResponse)
    def save_image(ref_id, category, file_name, desc,file_data):

        rsp = AddFileResponse()
        rsp.code = '033'
        rsp.msg = "Add image infomation  ok!"
        rsp.f_id = None

        image = FileInfo()
        image.ref_id = ref_id
        image.category = category
        filename = str(uuid.uuid4()) + file_name[file_name.rfind('.'):]
        file_path = save_file(filename, file_data, '02')
        image_info = get_image_info(file_path)

        image_type = image_info['type']
        width, heigth = image_info['image_size']
        file_size = image_info['file_size']

        if image_type not in ['JPEG', 'BMP', 'GIF', 'PPM', 'PNG']:
            rsp.code = '030'
            rsp.msg = "your upload file is not image type!"
            return rsp

        if width > config.image_limit['width'] or heigth > config.image_limit['higth']:
            rsp.code = '031'
            rsp.msg = "your upload file' width * higth must less than (%s x %s)! " % (config.image_limit['width'],config.image_limit['higth'])
            return rsp

        if file_size > config.image_limit['file_size']:

            rsp.code = '032'
            rsp.msg = "your upload file' size can't larger than %s ! " % (config.image_limit['file_size'])
            return rsp

        image.file_path = file_path
        image.desc = desc
        pk_id = add_file(image)
        if pk_id:
            rsp.f_id = pk_id
            return rsp
        else:
            rsp.code = '034'
            rsp.msg = "Add image infomation  failed!"
            return rsp

    @spyne.srpc(Unicode, Unicode, Unicode, _returns=AddCustomServiceResponse)
    def save_product_custom_service(product_code,phone_num,address):
        custom_service = CustomServiceInfo()
        custom_service.product_code = product_code
        custom_service.address = address
        custom_service.phone_num = phone_num
        pk_id = add_custom_service_info(custom_service)
        rsp = AddCustomServiceResponse()
        if pk_id:
            rsp.code = '040'
            rsp.msg = "Add product's customer service infomation ok!"
            rsp.c_id = pk_id
            return rsp
        else:
            rsp.code = '041'
            rsp.msg = "Add product's customer service infomation failed!"
            return rsp


    @spyne.srpc(Unicode, _returns=GetProductResponse)
    def get_product_info_old(product_code):
        response = GetProductResponse()
        response.code = '080'
        import json
        a = {'name': 'zhanghe', 'age': 20}
        a_json = json.dumps(a)
        response.msg = a_json

        # response.msg = 'query product info ok!!'

        if product_code is not None or product_code != '':

            result = get_product_by_id(product_code)
            product = ProductInfos()
            if result[0] == 1:
                product_base = result[1]

                product.id = product_base.id
                product.product_code = product_base.product_code
                product.guide_price = product_base.guide_price
                product.pack_list = product_base.pack_list

                print product
                product.images = []
                images = get_file(product_base.id, '01')

                if images[0] != 0:
                    for item in images[1]:
                        image = ImageInfo()
                        image.id = item.id
                        image.ref_id = item.ref_id
                        file_path = item.file_path
                        image_info = get_file_data(file_path)
                        image.file_name = image_info[0]
                        file_name = image_info[0]
                        image.file_data = image_info[1]
                        product.images.append(image)
                print product
                custom_services = get_custom_service_by_product_code(product_code)
                product.services =[]
                if custom_services[0] != 0:
                    print '--'
                    for item in custom_services[1]:
                        custom_service = CustomService()
                        custom_service.id = item.id
                        custom_service.address = item.address
                        custom_service.phone_num = item.phone_num
                        custom_service.product_code = item.product_code
                        product.services.append(custom_service)

                company_result = get_company_by_company_id(product_base.company_id)
                print company_result
                product.company = None
                if company_result[0] != 0:
                    comp = company_result[1]
                    company = Company()
                    company.company_id = comp.company_id
                    company.name = comp.name
                    company.website = comp.website
                    company.service_phone = comp.service_phone
                    print company
                    company_images_result = get_file(product_base.company_id, '02')
                    print company_images_result
                    company.images=[]

                    if company_images_result[0] !=0:
                        for item in company_images_result[1]:
                            image = ImageInfo()
                            image.id = item.id
                            image.ref_id = item.ref_id
                            file_path = item.file_path
                            image_info = get_file_data(file_path)
                            image.file_name = image_info[0]
                            image.file_data = image_info[1]
                            company.images.append(image)
                    product.company = company
                print product
            response.product = product
        return response

    @spyne.srpc(Unicode, _returns=Unicode)
    def get_product_info(product_code):
        response = {}
        response['code'] = '080'
        response['msg'] = 'query product info ok!!'
        #
        # a_json = json.dumps(a)
        # response.msg = a_json


        if product_code is not None or product_code != '':

            result = get_product_by_id(product_code)
            product = {}
            if result[0] == 1:
                goods = {}
                product_base = result[1]

                goods['id'] = product_base.id
                goods['product_code'] = product_base.product_code
                goods['name'] = product_base.name
                goods['guide_price'] = product_base.guide_price
                goods['introduce'] = product_base.introduce
                goods['detail_info'] = product_base.detail_info
                goods['pack_list'] = product_base.pack_list
                product['goods'] = goods

                product['images'] = []
                images = get_file(product_base.id, '01')

                if images[0] != 0:
                    for item in images[1]:
                        image = {}
                        image['id'] = item.id
                        image['ref_id'] = item.ref_id
                        image['desc'] = item.desc
                        file_path = item.file_path
                        image_info = get_file_data(file_path)
                        image['file_name'] = image_info[0]
                        file_name = image_info[0]
                        image['file_data'] = image_info[1]
                        product['images'].append(image)

                custom_services = get_custom_service_by_product_code(product_code)
                product['services'] =[]
                if custom_services[0] != 0:
                    print '--'
                    for item in custom_services[1]:
                        custom_service = {}
                        custom_service['id'] = item.id
                        custom_service['address'] = item.address
                        custom_service['phone_num'] = item.phone_num
                        custom_service['product_code'] = item.product_code
                        product['services'].append(custom_service)

                company_result = get_company_by_company_id(product_base.company_id)
                print company_result

                if company_result[0] != 0:
                    comp = company_result[1]
                    company = {}
                    company['company_id'] = comp.company_id
                    company['name'] = comp.name
                    company['address'] = comp.address
                    company['website'] = comp.website
                    company['service_phone'] = comp.service_phone
                    print company
                    company_images_result = get_file(product_base.company_id, '02')
                    print company_images_result
                    # company['images']= []
                    #
                    # if company_images_result[0] !=0:
                    #     for item in company_images_result[1]:
                    #         image = {}
                    #         image['id'] = item.id
                    #         image['ref_id'] = item.ref_id
                    #         file_path = item.file_path
                    #         image_info = get_file_data(file_path)
                    #         image['file_name'] = image_info[0]
                    #         image['file_data'] = image_info[1]
                    #         company['images'].append(image)
                    product['company'] = company
                # print product
            else:
                response['code'] = '081'
                response['msg'] = "can't acquire the prpduct info"
            response['product'] = product
            rsp_json = json.dumps(response)
            print rsp_json
        return rsp_json
