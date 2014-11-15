# -*- coding: utf-8 -*-
""" Role models."""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-22 11:06:15"

import datetime
from app.extensions import db

class RoleInfo(db.Model):
    """ Role information."""
    __tablename__ = 'role_info'
    id = db.Column(db.Integer, primary_key=True)
    role_code = db.Column(db.String(20), nullable=False, unique=True)
    role_name = db.Column(db.String(50), nullable=False, unique=True)
    role_desc = db.Column(db.String(100))
    creator = db.Column(db.Integer, db.ForeignKey('user_info.id', use_alter=True, name='fk_create_roleinfo_user_id'))
    creator_obj = db.relationship('UserInfo', primaryjoin='RoleInfo.creator==UserInfo.id')
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

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
        return '<RoleInfo>'
