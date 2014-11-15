# -*- coding: utf-8 -*-
"""
  the flow node mode
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-9-01"

from app.extensions import db


class FlowNode(db.Model):

    __tablename__ = 'flow_node'

    flow_node_id = db.Column(db.Integer, primary_key= True)
    flow_id = db.Column(db.Integer)
    flow_node_name = db.Column(db.String(50))
    flow_node_desc = db.Column(db.String(500))
    flag = db.Column(db.CHAR(1))  # 1 start node 0 process node