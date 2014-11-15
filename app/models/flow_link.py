# -*- coding: utf-8 -*-
"""
  the flow-link mode
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-9-01"


from app.extensions import db


class FlowLink(db.Model):

    __tablename__ = 'flow_link'

    flow_link_id = db.Column(db.Integer, primary_key=True)
    flow_id = db.Column(db.Integer)
    # link_name = db.Column(db.Integer)
    previous_node_id = db.Column(db.Integer)
    next_node_id = db.Column(db.Integer)
