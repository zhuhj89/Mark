# -*- coding: utf-8 -*-
""" Role permissions relational mapping model."""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-22 11:06:15"

import datetime
from app.extensions import db

class RoleAuthInfo(db.Model):
    """ Role permissions relational mapping classes."""
    __tablename__ = 'role_auth_info'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)
    auth_id = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.Integer, nullable=False, default=0)
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
        return '<RoleAuthInfo>'