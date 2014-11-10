# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-25"


from spyne.error import ResourceNotFoundError
from sqlalchemy import and_
import logging
from app import db
import datetime


class AuditRecord(db.Model):
    """Contact information."""


    __tablename__ = 'audit_record'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    domain_name = db.Column(db.String(255))
    # status of the record，0: has not audit 1:auditing the record 2 # :the record is success audit 3:failed audit
    status = db.Column(db.String(1))
    auditer = db.Column(db.String(32))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())  # create time
    audit_time = db.Column(db.DateTime)   # the time  of audited time
    audit_desc = db.Column(db.String(255))  # description of aduit



def add_audit_record(audit_record):
    """ Creating audit_record information.

        Args:
            audit_record: audit_record information.
    """

    if audit_record.id is None:
        db.session.add(audit_record)
        db.session.flush()

    else:

        info = AuditRecord.query.get(audit_record.id)

        if info is None:
            raise ResourceNotFoundError('audit_record.id=%d' % audit_record.id)
        else:
            AuditRecord.merge(audit_record)
    db.session.commit()
    return audit_record.id


def get_record_by_domain_status(domain_name, status):

    record = AuditRecord.query.filter(and_(AuditRecord.domain_name == domain_name, AuditRecord.status == status)).scalar()

    return record

