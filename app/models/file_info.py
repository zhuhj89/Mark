# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-21"


from app import db
from spyne.error import ResourceNotFoundError
from sqlalchemy import and_


class FileInfo(db.Model):
    """Contact information."""


    __tablename__ = 'file_info'

    id = db.Column(db.Integer, primary_key=True)
    ref_id = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(128))
    ######################################
    # date: 2014-10-27 14:02:43
    # version:
    # maintainer:
    # email:
    # context: Update Orm class FileInfo
    # add attribute desc
    ######################################
    desc = db.Column(db.String(500))
    category = db.Column(db.String(2))   # '01' --- 产品   '02' --- 公司   '03'--营业执照 '04' --编码证书

def add_file(file_info):
    """ Creating contact information.

        Args:
            contact_info: Contact information.
    """

    if file_info.id is None:
        db.session.add(file_info)
        db.session.flush()

    else:

        info = FileInfo.query.get(file_info.id)

        if info is None:
            raise ResourceNotFoundError('file_info.id=%d' % file_info.id)
        else:
            db.session.merge(file_info)
    db.session.commit()
    return file_info.id


def get_file(ref_id, category):

    files = FileInfo.query.filter(and_(FileInfo.ref_id == ref_id, FileInfo.category == category)).all()
    if files is None:
        return [0, None]
    else:
        return [1, files]
