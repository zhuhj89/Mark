# -*- coding: utf-8 -*-
"""
  the flow mode
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-9-01"

from app import db


class Flow(db.Model):

    __tablename__ = 'flow'

    flow_id = db.Column(db.Integer, primary_key=True)
    flow_code = db.Column(db.CHAR(3))
    flow_name = db.Column(db.String(50))
    flow_desc = db.Column(db.String(512))