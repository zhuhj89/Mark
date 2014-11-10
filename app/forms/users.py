# -*- coding: utf-8 -*-
""" User form, including user login, user logout, add users, 
    change user, change user password.
"""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-22 14:00:45"

from app.models import RoleInfo
from app.models import UserInfo
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import RadioField
from wtforms import DateTimeField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Regexp
from wtforms.validators import InputRequired
from wtforms.validators import EqualTo
from wtforms.validators import Optional
from wtforms.validators import ValidationError


class LoginForm(Form):
    """ User login form."""
    username = StringField(u'账户', validators=[DataRequired(message=u'请输入用户名')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'请输入密码')])
    remember_me = BooleanField(u'记住我', default=False)


class AddUserForm(Form):
    """ Add user form."""
    username = StringField(u'账号', validators=[DataRequired(message=u'请输入用户名')])
    password = PasswordField(u'密码', validators=[InputRequired(message=u'请输入密码'), EqualTo('confirm',message=u'确认密码不匹配。')])
    confirm = PasswordField(u'确认密码')
    # role_id = SelectField(u'角色', coerce=int, choices=[(role.id, role.role_name) for role in RoleInfo.query.filter_by().all()])
    status = RadioField(u'状态', choices=[('1', u'启用'), ('0', u'禁用')], validators=[DataRequired(message=u'请选择')])
    name = StringField(u'名称', validators=[DataRequired(message=u'请输入名称')])
    email = StringField(u'邮箱', validators=[DataRequired(message=u'请输入邮箱地址'), Email(message=u'请输入正确的邮箱格式。')])
    phone = StringField(u'电话', validators=[DataRequired(message=u'请输入电话号码'), Regexp(regex='(^(\d{3,4}-)?\d{7,8})$|(1[0-9]{10})', message=u'请输入正确的电话号码格式。')])


    def validate_username(self, field):
        """ Verify username value exists, username value is unique.

            Args:
                form: Fixed form 
                field: Fixed Field
        """
        user = UserInfo.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError(u'账号已存在，请更换。')

class UpdateUserForm(Form):
    """ Update user form."""
    # role_id = SelectField(u'角色', coerce=int, choices=[(role.id, role.role_name) for role in RoleInfo.query.filter_by().all()])
    status = RadioField(u'状态', choices=[('1', u'启用'), ('0', u'禁用')], validators=[DataRequired()])
    name = StringField(u'名称', validators=[DataRequired()])
    email = StringField(u'邮箱', validators=[DataRequired(), Email(message=u'请输入正确的邮箱格式。')])
    phone = StringField(u'电话', validators=[DataRequired(), Regexp(regex='(^(\d{3,4}-)?\d{7,8})$|(1[0-9]{10})', message=u'请输入正确的电话号码格式。')])


class UpdatePasswordForm(Form):
    """ Update user password form."""
    current_password = PasswordField(u'当前密码', validators=[DataRequired()])
    password = PasswordField(u'新的密码', validators=[InputRequired(), EqualTo('confirm',message=u'确认密码不匹配。')])
    confirm = PasswordField(u'确认密码')