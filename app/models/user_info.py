# -*- coding: utf-8 -*-
""" User model is used to add, edit, query, delete user information."""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-22 11:06:15"

import datetime
from app.extensions import db


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role_info.id', use_alter=True,name='fk_user_role_id'))
    role = db.relationship('RoleInfo', backref='users',foreign_keys=[role_id])
    status = db.Column(db.Integer, nullable=False, default=1)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('user_info.id', use_alter=True, name='fk_create_userinfo_user_id'))
    creator_obj = db.relationship('UserInfo', backref='userinfos', remote_side=id)
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
        return '<UserInfo %r>' % self.username
