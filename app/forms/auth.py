# -*- coding: utf-8 -*-
""" Permission form.
    Contains add permissions, update permissions, check permissions.
"""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-27 11:18:20"


from app.models.auth_info import AuthInfo
from flask.ext.wtf import Form
from wtforms import StringField,SelectField,RadioField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError


class AuthForm(Form):
    """ Permission form, setting roles have permission."""
    auth_name = StringField(u'权限名称',validators=[DataRequired(message=u'请输入权限名')])
    auth_code = StringField(u'权限代码',validators=[DataRequired(message=u'请输入权限代码')])
    auth_url = StringField(u'权限Url')
    auth_desc = StringField(u'权限说明')
    auth_leave = SelectField(u'菜单等级', choices=[('1', u'一级菜单'), ('2', u'二级菜单')], validators=[DataRequired(message=u'请选择')])
    # parent_auth_id = SelectField(u'上级菜单', coerce=int, choices=[(auth.id, auth.auth_name) for auth in AuthInfo.query.filter(AuthInfo.auth_leave==1).all()])
    nav_display = RadioField(u'是否导航栏显示', choices=[('1', u'是'), ('0', u'否')], validators=[DataRequired(message=u'请选择')])

    def validate_auth_code(form, field):
        """ Verify auth_code value exists, auth_code value is unique.

            Args:
                form: Fixed form 
                field: Fixed Field
        """
        auth = AuthInfo.query.filter_by(auth_code=field.data).first()
        if auth:
            raise ValidationError(u'权限代码已存在，请更换。')


class AuthUpdateForm(Form):
    """ Permission form, setting roles have permission."""
    auth_name = StringField(u'权限名称',validators=[DataRequired(message=u'请输入权限名')])
    auth_url = StringField(u'权限Url')
    auth_desc = StringField(u'权限说明')