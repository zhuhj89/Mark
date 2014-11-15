#coding=utf-8
import datetime
from app.extensions import db


class DomainPayRecord(db.Model):
    __tablename__ = 'domain_pay_record'
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, nullable=False)
    domain_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.DECIMAL(8, 2), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
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
        return '<DomainPayRecord>'
