#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-18"
"""
extends moudles
"""
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


__all__ = ['db', 'login_manager']
db = SQLAlchemy()
login_manager = LoginManager()
