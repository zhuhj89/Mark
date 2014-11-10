# -*- coding: utf-8 -*-
""" The role of information management classes.
    add role, change role, delete role, view the role.
"""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-27 11:02:34"


from config import Page_Count
from app import db
from app import mark_app
from flask import Module
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import render_template
from flask.ext.login import current_user
from flask.ext.login import login_required
from app.forms.role import RoleForm
from app.models.role_info import RoleInfo
from app.models.user_info import UserInfo
from app.models.role_auth_info import RoleAuthInfo


role = Module(__name__)


@mark_app.route('/role/addrole/', methods=['GET', 'POST'])
@login_required
def add_role():
    """ Add role information

        return:
            Success message. 
            Add page.
    """
    role_form = RoleForm()
    if request.method == 'POST':
        if role_form.validate_on_submit():
            role = RoleInfo()
            role_form.populate_obj(role)
            role.creator = current_user.id
            db.session.add(role)
            db.session.commit()
            flash(u'角色添加成功。')
            return redirect(url_for('query_role'))
    return render_template('/role/add_role.html', form=role_form, creator_value=current_user.username)


@mark_app.route('/role/updaterole/<role_id>/', methods=['GET', 'POST'])
@login_required
def update_role(role_id):
    """ Modify role information.

        Args:
            role_id: role identifier.

        return:
            Success message. 
            modify page.
    """
    update_role = RoleInfo.query.filter_by(id=role_id).first()
    role_form = RoleForm(obj = update_role)
    if request.method == 'POST':
        if role_form.validate_on_submit():
            role_form.populate_obj(update_role)
            db.session.commit()
            flash(u'角色更新成功。')
            return redirect(url_for('query_role'))
    return render_template('/role/update_role.html', form=role_form, update_role=update_role)


@mark_app.route('/role/queryrole/')
@mark_app.route('/role/queryrole/<int:page>/')
@login_required
def query_role(page=1):
    """ Paging query role information.

        Args:
            page: Pages.

        return:
            role list page.
    """
    role_page_obj = RoleInfo.query.filter_by().paginate(page, Page_Count)
    role_page_url = lambda page : url_for('query_role', page=page)
    return render_template('/role/query_role.html', role_page_obj=role_page_obj, role_page_url=role_page_url)


@mark_app.route('/role/deleterole/<role_id>/')
@login_required
def delete_role(role_id):
    """ Delete role information.

        Args:
            role_id: role identifier.

        return:
            role to delete the results.
    """
    user = UserInfo.query.filter_by(role_id=role_id).first()
    if user:
        flash(u'角色关联了用户，不能删除。')
        return redirect(url_for('query_role'))
    ######################################
    # date: 2014-11-05 14:02:43
    # version:
    # maintainer:
    # email:
    # context: modify delete_role function
    # role ref to auth the relationship is many to  many
    # if delete the role the role auth must delete
    ######################################
    RoleAuthInfo.query.filter_by(role_id=role_id).delete()
    # role_auth = RoleAuthInfo.query.filter_by(role_id=role_id).first()
    # if role_auth:
    #     flash(u'角色关联了权限，不能删除')
    #     return redirect(url_for('query_role'))

        
    RoleInfo.query.filter_by(id=role_id).delete()
    db.session.commit()
    flash(u'角色删除成功。')
    return redirect(url_for('query_role'))