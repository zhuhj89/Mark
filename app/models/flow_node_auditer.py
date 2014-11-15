# -*- coding: utf-8 -*-
"""
  the flow-node-auditer mode
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-9-01"


from app.extensions import db


class FlowNodeAuditer(db.Model):

    __tablename__ = 'flow_node_auditer'

    node_auditer_id = db.Column(db.Integer, primary_key=True)
    flow_node_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)