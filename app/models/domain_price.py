#coding=utf-8
import datetime
from app.extensions import db


class DomainPrice(db.Model):
    __tablename__ = 'domain_price'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.DECIMAL(8, 2), nullable=False)
    pay_type = db.Column(db.Integer, nullable=False)
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
        return '<DomainPrice>'