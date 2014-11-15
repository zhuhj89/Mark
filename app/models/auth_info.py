# -*- coding: utf-8 -*-
""" Permissions model."""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-22 11:06:15"

import datetime
from app.extensions import db


class AuthInfo(db.Model):
    """ Permission information."""
    __tablename__ = 'auth_info'
    id = db.Column(db.Integer, primary_key=True)
    auth_code = db.Column(db.String(20), nullable=False, unique=True)
    auth_name = db.Column(db.String(50), nullable=False, unique=True)
    auth_url = db.Column(db.String(1000))
    auth_desc = db.Column(db.String(100))
    creator = db.Column(db.Integer, db.ForeignKey('user_info.id', use_alter=True, name='fk_create_auth_user_id'))
    creator_obj = db.relationship('UserInfo', backref='authinfos', primaryjoin='AuthInfo.creator==UserInfo.id')
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    parent_auth_id = db.Column(db.Integer,default=0)
    auth_leave = db.Column(db.Integer)  # 1 - nav
    nav_display = db.Column(db.Integer)

    def is_authenticated(self):
        """ Flask-login plugin function."""
        return True

    def is_active(self):
        """ Flask-login plugin function."""
        return True

    def is_anonymous(self):
        """ Flask-login plugin function."""
        return False

    def get_id(self):
        """ Flask-login plugin function."""
        return unicode(self.id)

    def __repr__(self):
        return '<AuthInfo>'