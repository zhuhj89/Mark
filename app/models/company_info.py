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

from app.extensions import db
from spyne.error import ResourceNotFoundError


class CompanyInfo(db.Model):
    """company information."""

    __tablename__ = 'company_info'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    ######################################
    # date: 2014-10-27 14:02:43
    # version:
    # maintainer:
    # email:
    # context: Update Orm class FileInfo
    # add attribute address
    ######################################
    address = db.Column(db.String(500))
    website = db.Column(db.String(32))
    service_phone = db.Column(db.String(20))
    product = db.relationship('ProductInfo', backref='company', uselist=False)

def add_company_info(company):
    """ Creating contact information.

        Args:
            contact_info: Contact information.
    """

    if company.id is None:
        db.session.add(company)
        db.session.flush()

    else:

        info = CompanyInfo.query.get(company.id)

        if info is None:
            raise ResourceNotFoundError('file_info.id=%d' % company.id)
        else:
            db.session.merge(company)
    db.session.commit()
    return company.id


def get_company_by_company_id(company_id):
    company = CompanyInfo.query.filter(CompanyInfo.company_id == company_id).scalar()
    if company is None:
        return [0, None]
    else:
        return [1, company]
