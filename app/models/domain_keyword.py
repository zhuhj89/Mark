#coding=utf-8
import datetime
from app.extensions import db

class DomainKeyword(db.Model):
    __tablename__ = 'domain_keyword'
    id = db.Column(db.Integer, primary_key=True)
    keyword_type = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(100), nullable=False)
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
        return '<DomainKeyword>'