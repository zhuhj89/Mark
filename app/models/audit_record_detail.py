# -*- coding: utf-8 -*-
"""
  the audit record detail  mode
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-9-01"


from app.extensions import db


class AuditRecordDetail(db.Model):

    __tablename__ = 'audit_record_detail'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer)
    flow_node_id = db.Column(db.Integer)
    auditer = db.Column(db.String(32))
    audit_desc = db.Column(db.String(500))
    status = db.Column(db.String(1))  # '1' not approve  '2' will approve '3' approve agree '4' approve not agree
    audit_time = db.Column(db.DateTime)