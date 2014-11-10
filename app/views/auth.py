# -*- coding: utf-8 -*-
""" Permissions management classes.
    Contains add permissions, update permissions, delete permissions, check permissions.
"""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "(2014-8-27 15:53:44)"


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
from app.forms.auth import AuthForm
from app.forms.auth import AuthUpdateForm
from app.models.auth_info import AuthInfo
from app.models.role_auth_info import RoleAuthInfo

auth = Module(__name__)

@mark_app.route('/auth/addauth/', methods=['GET', 'POST'])
@login_required
def add_auth():
    """ Add permissions information.

        return:
            Success message. 
            Add page.
    """
    auth_form = AuthForm()
    parent_auths = AuthInfo.query.filter(AuthInfo.auth_leave == 1).all()
    if request.method == 'POST':
        if auth_form.validate_on_submit():
            parent_auth_id = request.form['parent_auth_id']
            auth_leave = request.form['auth_leave']
            print parent_auth_id
            auth = AuthInfo()
            auth_form.populate_obj(auth)
            auth.creator = current_user.id
            if auth_leave == '2':
                auth.parent_auth_id = parent_auth_id
            db.session.add(auth)
            db.session.flush()

            db.session.commit()
            flash(u'权限添加成功。')
            return redirect(url_for('query_auth'))

    return render_template('/auth/add_auth.html', form=auth_form, creator_value=current_user.username, parent_auths=parent_auths)


@mark_app.route('/auth/updateauth/<auth_id>/', methods=['GET', 'POST'])
@login_required
def update_auth(auth_id):
    """ Modify permissions information.

        Args:
            auth_id: Permissions identifier.

        return:
            Success message. 
            modify page.
    """
    update_auth = AuthInfo.query.filter_by(id=auth_id).first()
    auth_update_form = AuthUpdateForm(obj = update_auth)
    if request.method == 'POST':
        if auth_update_form.validate_on_submit():
            auth_update_form.populate_obj(update_auth)
            db.session.commit()
            flash(u'权限更新成功。')
            return redirect(url_for('query_auth'))
    return render_template('/auth/update_auth.html', form=auth_update_form, update_auth=update_auth)

@mark_app.route('/auth/queryauth/')
@mark_app.route('/auth/queryauth/<int:page>/')
@login_required
def query_auth(page=1):
    """ Paging query permissions information.

        Args:
            page: Pages.

        return:
            Permissions list page.
    """
    auth_page_obj = AuthInfo.query.filter_by().paginate(page, per_page=Page_Count)
    auth_page_url = lambda page : url_for('query_auth', page=page)
    return render_template('/auth/query_auth.html', auth_page_obj=auth_page_obj, auth_page_url=auth_page_url)


@mark_app.route('/auth/deleteauth/<auth_id>/')
@login_required
def delete_auth(auth_id):
    """ Delete permissions information.

        Args:
            auth_id: Permissions identifier.

        return:
            Permission to delete the results.
    """
    role_auth = RoleAuthInfo.query.filter_by(auth_id=auth_id).first()
    if role_auth:
        flash(u'权限关联了角色，不能删除')
        return redirect(url_for('index'))

    AuthInfo.query.filter_by(id=auth_id).delete()
    db.session.commit()
    flash(u'权限删除成功。')
    return redirect(url_for('query_auth'))