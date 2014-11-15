# -*- coding: utf-8 -*-
""" Role form, including add role, change role."""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-27 11:18:20"


from app.models.role_info import RoleInfo
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

class RoleForm(Form):
    """ Role form. Add Roles and modify the role to use."""
    role_name = StringField(u'角色名称', validators = [DataRequired(message=u'请输入角色名')])
    role_code = StringField(u'角色代码', validators = [DataRequired(message=u'请输入角色代码')])
    role_desc = StringField(u'角色说明')

    def validate_role_code(form, field):
        """ Verify role_code value exists, role_code value is unique.

            Args:
                form: Fixed form 
                field: Fixed Field
        """
        role = RoleInfo.query.filter_by(role_code=field.data).first()
        if role:
            raise ValidationError(u'角色代码已存在，请更换角色代码')


