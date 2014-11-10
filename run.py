#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" application run file"""
__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"

import sys
import logging
from app import mark_app
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log/myapp.log',
                filemode='w+')
console = logging.StreamHandler()
logging.getLogger('sqlalchemy.engine.base.Engine').addHandler(console)


# reload(sys)
# sys.setdefaultencoding('utf-8')
mark_app.run(host='127.0.0.1', port=8080, debug=True)
