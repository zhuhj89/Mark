#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" webservice client test file
"""
__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2007, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"
from soaplib.client import make_service_client
from soaplib.serializers.binary import Attachment
from webservice.ws_server import NiotWebService

client = make_service_client('http://localhost:7777/', NiotWebService())
print client.simple_method("test_str")
print client.file_upload(Attachment(fileName='G:/test.jpg'))