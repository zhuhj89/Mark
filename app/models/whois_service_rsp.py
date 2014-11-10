# -*- coding: utf-8 -*-
"""
  the whois query Rsp moudle
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-05"

from spyne.model.primitive import Unicode, DateTime
from spyne.model.complex import ComplexModel,Array


class ContactInfo(ComplexModel):
    __namespace__ = 'tns'
    type = Unicode(20)
    registrant = Unicode(250)
    email = Unicode(50)


class DomainInfo(ComplexModel):
    __namespace__ = 'tns'
    name = Unicode(50)
    registrar = Unicode(100)
    registrant = Unicode(250)
    email = Unicode(50)
    # contacts = Array(ContactInfo)
    reg_date = DateTime()
    exp_date = DateTime()
    name_server = Unicode(500)
    status = Unicode(500)


class WhoisQueryRsp(ComplexModel):
    __namespace__ = 'tns'
    return_code = Unicode(3)
    return_msg = Unicode(500)
    result = DomainInfo
