# -*- coding: utf-8 -*-
"""
  the encrypt utils
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-26"
import hashlib


def md5(str):

    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()



# print md5('admin')