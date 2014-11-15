# -*- coding: utf-8 -*-
""" Role permissions map form."""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-27 11:18:20"


from app.models.auth_info import AuthInfo
from app.models.role_auth_info import RoleAuthInfo
from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import SelectMultipleField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from wtforms.widgets import ListWidget
from wtforms.widgets import CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    """ A multiple-select, except displays a list of checkboxes.

        Iterating the field will produce subfields, allowing custom rendering of
        the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class RoleAuthForm(Form):
    """ Modify role permissions to use."""
    # auth_list = MultiCheckboxField(u'选择权限', choices=[(str(auth.id), auth.auth_name) for auth in AuthInfo.query.filter_by().all()])
    pass
