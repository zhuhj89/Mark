#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-11-14"

import logging,logging.config, yaml
from logging.handlers import TimedRotatingFileHandler
logging.config.dictConfig(yaml.load(open('logging.conf')))
logfile = logging.getLogger('file')
logconsole = logging.getLogger('console')

logger = logging.getLogger('d_file')
logger.setLevel(logging.DEBUG)
file_handler = TimedRotatingFileHandler('mark', 'S', 1, 0)
file_handler.suffix = '%Y%m%d-%H%M%S.log'
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)