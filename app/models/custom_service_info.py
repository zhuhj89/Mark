# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-19"

from app import db
from spyne.error import ResourceNotFoundError



class CustomServiceInfo(db.Model):
    """Contact information."""


    __tablename__ = 'custom_service_info'

    id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String(20))
    address = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('product_info.id'), nullable=False)

def add_custom_service_info(custom_service_info):
    """ Creating contact information.

        Args:
            contact_info: Contact information.
    """

    if custom_service_info.id is None:
        db.session.add(custom_service_info)
        db.session.flush()

    else:

        info = CustomServiceInfo.query.get(custom_service_info.id)

        if info is None:
            raise ResourceNotFoundError('file_info.id=%d' % custom_service_info.id)
        else:
            db.session.merge(custom_service_info)
    db.session.commit()
    return custom_service_info.id

def get_custom_service_by_product_code(product_code):
    custom_service = CustomServiceInfo.query.filter(CustomServiceInfo.product_code == product_code).all()
    if len(custom_service) == 0:
        return [0, None]
    else:
        return [1, custom_service]
