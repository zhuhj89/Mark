# -*- coding: utf-8 -*-
""" """
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-27 11:02:34"


from app import db
from app import mark_app
from flask import Module
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import flash
from flask import render_template
from flask.ext.login import current_user
from flask.ext.login import login_required
from app.models.role_info import RoleInfo
from app.models.role_auth_info import RoleAuthInfo
from app.forms.role_auth import RoleAuthForm


role_auth = Module(__name__)


@mark_app.route('/roleauth/setroleauth/<role_id>', methods=['GET', 'POST'])
@login_required
def set_role_auth(role_id):
    """ Setting role permissions.

        Args:
            role_id: role identifier.

        return:
            Success message. 
            Set permissions page.
    """
    role = RoleInfo.query.filter_by(id=role_id).first()
    current_auth_list =[str(role_auth.auth_id) for role_auth in RoleAuthInfo.query.filter_by(role_id=role_id).all()]
    # Create a permission form and set the default value.

    auth_list = db.session.execute('SELECT a.id,a.auth_name,a.auth_code,a.parent_auth_id,a.auth_leave, ra.role_id '
                                   'FROM auth_info a LEFT JOIN  '
                                   '(SELECT * FROM role_auth_info WHERE role_id =:role_id) ra '
                                   'ON  ra.auth_id = a.id', {"role_id": role_id}).fetchall()



    # role_auth_form = RoleAuthForm(auth_list=current_auth_list)
    # if request.method == 'POST' and role_auth_form.validate():

    if request.method == 'POST':
        # print role_auth_form.auth_list.data
        RoleAuthInfo.query.filter_by(role_id=role_id).delete()

        auth_ids = request.form.getlist('auth_id')
        print auth_ids
        for auth_id in auth_ids:
            role_auth = RoleAuthInfo()
            role_auth.role_id = role_id
            role_auth.auth_id = auth_id
            db.session.add(role_auth)
            
        flash(u'权限设置成功。')
        db.session.commit()
        return redirect(url_for('set_role_auth', role_id=role_id))
    # return render_template('/role/set_role_auth.html', form=role_auth_form, role=role, user=current_user,auth_list=auth_list)
    return render_template('/role/set_role_auth.html', role=role, user=current_user,auth_list=auth_list)