#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" database create file
"""
__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"
import app
# from config import SQLALCHEMY_MIGRATE_REPO, SQLALCHEMY_DATABASE_URI
from app.models import CompanyInfo,ProductInfo
app.db.create_all()
# if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
#     api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
#     api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
# else:
#     api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))