# -*- coding: utf-8 -*-
""" agent forms
"""
from gettext import gettext
from app.models import DomainPrice, AgentInfo

__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2007, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, DecimalField, ValidationError,FloatField
from wtforms.validators import DataRequired, Email, URL,NumberRange


class AgentForm(Form):
    comp_name = StringField(u'注册商公司名', validators=[DataRequired(message=u'请输入注册商公司名')])
    email = StringField(u'邮箱', validators=[DataRequired(message=u'请输入邮箱地址'), Email(message=u'请输入正确的邮箱格式')])
    phone = StringField(u'联系电话', validators=[DataRequired(message=u'请输入联系电话')])
    url = StringField(u'注册商网址', validators=[DataRequired(message=u'请输入注册商网址')])
    abuse_email = StringField(u'紧急联系邮箱', validators=[DataRequired(message=u'请输入邮箱地址'), Email(message=u'请输入正确的邮箱格式')])
    abuse_phone = StringField(u'紧急联系电话', validators=[DataRequired(message=u'请输入紧急联系电话')])

class AddAgentForm(AgentForm):
    agent_name = StringField(u'注册商用户名', validators=[DataRequired(message=u'请输入注册商用户名')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'请输入密码')])
    balance_remind = DecimalField(u'余额提醒值', validators=[DataRequired(u'请输入余额提醒值'),NumberRange(min=0,message=u'金额必须大于0')])
    domain_price_id = SelectField(u'域名价格', coerce=int,
                                  choices=[(p.id, str(p.price) + '/' + u'年' if p.pay_type == 1 else str(p.price) + '/' + u'月')
                                           for p in DomainPrice.query.all()])

    def validate_agent_name(self, field):
        ai = AgentInfo.query.filter_by(agent_name=field.data).first()
        if ai:
            raise ValidationError, gettext(u'该注册商名已存在')

class UpdateRemindForm(Form):
    agent_name = StringField(u'注册商', validators=[DataRequired()])
    balance_remind = FloatField(u'余额提醒值', validators=[DataRequired(message=u'请正确输入金额数字'),NumberRange(min=0,message=u'金额必须大于0')])