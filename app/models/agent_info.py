# -*- coding: utf-8 -*-
""" agent model
"""
__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2007, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"
import datetime
from app import db


class AgentInfo(db.Model):

    __tablename__ = 'agent_info'
    id = db.Column(db.Integer, primary_key=True)
    agent_name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    comp_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    balance_remind = db.Column(db.DECIMAL(8, 2), nullable=False)
    domain_price_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    abuse_email = db.Column(db.String(255), nullable=False)
    abuse_phone = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.DECIMAL(8, 2), nullable=False, default=0)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
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
        return '<AgentInfo %r>' % self.agent_name