# -*- coding: utf-8 -*-
""" agent account record model
"""
__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2007, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"
import datetime
from app.extensions import db


class AgentAccountRecord(db.Model):
    __tablename__ = 'agent_account_record'
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.DECIMAL(8, 2), nullable=False)
    balance = db.Column(db.DECIMAL(8, 2), nullable=False)
    operate = db.Column(db.Integer, nullable=False)
    record_desc = db.Column(db.String(200))
    creator = db.Column(db.Integer, nullable=False, default=0)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<AgentAccountRecord>'