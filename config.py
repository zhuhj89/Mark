# -*- coding: utf-8 -*-
""" config file
"""
__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2007, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"
import os
basedir = os.path.abspath(os.path.dirname(__file__))

Page_Count = 3

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/db_mark'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
