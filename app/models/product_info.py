# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-20"


from app import db
from spyne.model.complex import Iterable, ComplexModel

class ProductInfo(db.Model):
    """Contact information."""


    __tablename__ = 'product_info'
    __namespace__ = 'tns'
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(13))
    name = db.Column(db.String(32))
    introduce = db.Column(db.String(100))
    detail_info = db.Column(db.String(1000))
    guide_price = db.Column(db.String(8))
    pack_list = db.Column(db.String(500))
    company_id = db.Column(db.Integer, db.ForeignKey('company_info.id'), nullable=False)
    services = db.relationship('CustomServiceInfo', backref='product')

def add_product_info(product):
    """ Creating contact information.

        Args:
            contact_info: Contact information.
    """
    print product.product_code,type(product.product_code)
    info = ProductInfo.query.filter(ProductInfo.product_code == product.product_code).first()
    print info
    if info is None:

        db.session.add(product)
        db.session.flush()

    else:
        product.id = info.id
        db.session.merge(product)

    db.session.commit()
    return product.id

def get_product_by_id(product_code):

    product = ProductInfo.query.filter(ProductInfo.product_code == product_code).first()
    if product is None:
        return [0, None]
    else:
        return [1, product]


def update_product(product_code, parm):

    product = ProductInfo.query.filter(ProductInfo.product_code == product_code).first()
    product.company_id = parm['company_id']
    db.session.merge()
    return True