# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-21"

from spyne.model.primitive import Unicode
from spyne.model.primitive import UnsignedInteger32
from spyne.model.complex import ComplexModel
from spyne.model.binary import ByteArray
from app.models.file_info import FileInfo
from app.models.custom_service_info import CustomServiceInfo
from app.models.company_info import CompanyInfo
from spyne.model.complex import Array


class ImageInfo(ComplexModel):
    __namespace__ = 'tns'
    id = UnsignedInteger32()
    ref_id = UnsignedInteger32()
    file_name = Unicode(500)
    file_data = ByteArray()


class Company(ComplexModel):
    __namespace__ = 'tns'
    company_id = UnsignedInteger32()
    name = Unicode(32)
    website = Unicode(32)
    service_phone = UnsignedInteger32
    images = Array(ImageInfo)


class CustomService(ComplexModel):
    __namespace__ = 'tns'
    id = UnsignedInteger32()
    product_code = Unicode(13)
    phone_num = Unicode(32)
    address = Unicode(32)

class ProductInfos(ComplexModel):
    id = UnsignedInteger32()
    product_code = Unicode(13)
    name = Unicode(32)
    guide_price = Unicode(8)
    pack_list = Unicode(500)
    images = Array(ImageInfo)
    services = Array(CustomService)
    company = Company

class GetProductResponse(ComplexModel):
    __namespace__ = 'tns'
    code = Unicode(3)
    msg = Unicode(200)
    product = ProductInfos

class AddFileResponse(ComplexModel):
    __namespace__ = 'tns'

    code = Unicode(3)
    msg = Unicode(200)
    f_id = UnsignedInteger32


class AddCustomServiceResponse(ComplexModel):
    __namespace__ = 'tns'

    code = Unicode(3)
    msg = Unicode(200)
    c_id = UnsignedInteger32

class AddProductResponse(ComplexModel):
    __namespace__ = 'tns'

    code = Unicode(3)
    msg = Unicode(200)
    p_id = UnsignedInteger32


class AddCompanyResponse(ComplexModel):
    __namespace__ = 'tns'

    code = Unicode(3)
    msg = Unicode(200)
    company_id = UnsignedInteger32