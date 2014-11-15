# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-25"

from spyne.model.primitive import Unicode, DateTime

from spyne.model.complex import ComplexModel


class UploadDataRsp(ComplexModel):
    __namespace__ = 'tns'
    code = Unicode(3)
    msg = Unicode(200)

class QueryDomainStatRsp(ComplexModel):
    __namespace__ = 'tns'
    code = Unicode(3)
    msg = Unicode(200)
    domain_name = Unicode(50)
    audit_status = Unicode(1)
    audit_time = DateTime()
    reason = Unicode(500)


