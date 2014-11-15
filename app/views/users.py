# -*- coding: utf-8 -*-
""" User information management classes. 
    including user login, user logout, add users, change user, delete user, view the user.
"""
__author__ = "WangChuang"
__email__ = "WangChuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-22 14:00:45"

from sqlalchemy.exc import IntegrityError
from app.extensions import db,login_manager
from conf.config import Page_Count
from util.common import get_md5
# from util.logger import logfile
from app.models import UserInfo
from app.models import AuthInfo
from app.models import RoleInfo
from app.models import RoleAuthInfo
from app.forms.users import LoginForm
from app.forms.users import AddUserForm
from app.forms.users import UpdateUserForm
from app.forms.users import UpdatePasswordForm
from flask import render_template, current_app
from flask import request
from flask import session
from flask import flash
from flask import url_for
from flask import redirect,Blueprint
from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import logout_user
from flask.ext.login import current_user

users = Blueprint('users', __name__)

login_manager.login_view = 'users.login'
login_manager.login_message = u'需要登陆后才能访问本页'


@login_manager.user_loader
def load_user(uid):
    """ With user id to load user object.

        Args:
            uid: User id.

        return:
            User Object.
    """
    user = UserInfo.query.get(uid)
    return user


@users.route('/logout/')
@login_required
def logout():
    """ Logout users.

        return: 
            default page.
    """
    logout_user()
    flash(u'成功退出')
    return redirect(url_for('users.login'))


@users.route('/login/', methods=['GET', 'POST'])
def login():
    """ User login. 

        return: 
            login page.
            login message.
    """
    print current_app.config
    login_form = LoginForm()
    print "----------------"
    # logfile.info("Logging......")
    if request.method == 'POST':
        print "int post"
        if login_form.validate_on_submit():
            username = login_form.data['username']
            password = login_form.data['password']
            remember_me = login_form.data['remember_me']
            password_md5 = get_md5(password)
            print "-----------"
            current_login_user = UserInfo.query.filter_by(username=username).first()
            print "-----------"
            if current_login_user:
                print current_login_user.email
                if current_login_user.password == password_md5:
                    print current_login_user.status
                    if current_login_user.status == 0:
                        flash(u'用户已注销')
                    else:
                        login_user(current_login_user, remember=remember_me)

                        auth_list = AuthInfo.query.join(RoleAuthInfo, RoleAuthInfo.auth_id==AuthInfo.id).filter_by(role_id=current_user.role_id).order_by(RoleAuthInfo.auth_id).all()
                        # role_auth_list = db.session.execute('select a.id,a.parent_auth_id,a.auth_name,a.auth_url from role_auth_info as ra JOIN role_info as r on (ra.role_id = r.id) join auth_info as a on (ra.auth_id = a.id) \
                        #         where r.id =:role_id', {'role_id':current_user.role_id}).fetchall()
                        user_auths = []
                        for auth in auth_list:
                            user_auth = {}
                            user_auth['id'] = auth.id
                            user_auth['name']= auth.auth_name
                            user_auth['parent_auth_id'] = auth.parent_auth_id
                            user_auth['url'] = auth.auth_url
                            user_auth['auth_leave'] = auth.auth_leave
                            user_auth['nav_display'] = auth.nav_display
                            user_auths.append(user_auth)
                            # print user_auth
                        # print role_auth_list

                        # temp_name = ''
                        # for obj in role_auth_list:
                        #     role_name = obj.role_name
                        #     if temp_name == role_name:
                        #         continue
                        #     else:
                        #         auth_map = {}
                        #         for obj_check in role_auth_list:
                        #             if role_name == obj_check.role_name:
                        #                 auth_map[obj_check.auth_name] = obj_check.auth_url
                        #
                        #
                        #     user_auth[role_name] = auth_map;
                        #     temp_name = role_name
                        # print user_auths
                        session['user_auth'] = user_auths
                        # print user_auth
                        flash(u'登陆成功')
                        return render_template('/base.html')
                    return redirect(url_for('site.index'))
                else:
                    flash(u'账号和密码不匹配!')
            else:
                flash(u'用户不存在!')
    print "okkkkk"
    return render_template('/index.html', form=login_form)


@users.route('/adduser/', methods=['GET', 'POST'])
@login_required
def add_user():
    """ Add user information

        return:
            Success message. 
            Add page.
    """
    add_user_form = AddUserForm()
    roles = RoleInfo.query.filter_by().all()
    if request.method == 'POST':
        if add_user_form.validate_on_submit():
            password_md5 = get_md5(add_user_form.data['password'])
            role_id = request.form['role_id']
            add_user = UserInfo()
            add_user_form.populate_obj(add_user)
            add_user.password = password_md5
            add_user.creator = current_user.id
            add_user.role_id = role_id
            db.session.add(add_user)
            db.session.commit()
            flash(u'用户添加成功。')
            return redirect(url_for('users.query_user'))
    
    return render_template('/user/add_user.html', form=add_user_form, creator_value=current_user.username, roles=roles)

@users.route('/queryuser/')
@users.route('/queryuser/<int:page>/')
@login_required
def query_user(page=1):
    """ Paging query user information.

        Args:
            page: Pages.

        return:
            user list page.
    """
    user_page_obj = UserInfo.query.filter_by().paginate(page, per_page=Page_Count)
    user_page_url = lambda page : url_for('users.query_user', page=page)
    return render_template('/user/query_user.html', user_page_obj=user_page_obj, user_page_url=user_page_url)


@users.route('/updateuser/<user_id>/', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    """ Modify user information.

        Args:
            user_id: user identifier.

        return:
            Success message. 
            modify page.
    """
    update_user = UserInfo.query.filter_by(id=user_id).first_or_404()
    update_user_form = UpdateUserForm(obj=update_user)
    roles = RoleInfo.query.filter_by().all()
    if request.method == 'POST':
        if update_user_form.validate_on_submit():
            update_user_form.populate_obj(update_user)
            role_id = request.form['role_id']
            update_user.role_id = role_id
            db.session.commit()
            flash(u'用户信息修改成功。')
            return redirect(url_for('users.query_user'))

    return render_template('/user/update_user.html', form=update_user_form, update_user=update_user, roles=roles)

@users.route('/myinfo', methods=('GET', 'POST'))
@login_required
def user_info():

    user = UserInfo.query.filter_by(id=current_user.id).first_or_404()
    user_info_form = UpdateUserForm(obj=user)
    if request.method == 'POST':
        if user_info_form.validate_on_submit():
            user_info_form.populate_obj(user)
            # user.email = form.email.data
            # user.phone = form.phone.data
            # user.name = form.name.data
            db.session.commit()
            flash(u'修改成功')
            return redirect(url_for('site.base'))
    return render_template('/user/user_info.html', form=user_info_form, user=user)




@users.route('/updatepassword/', methods=['GET', 'POST'])
@login_required
def update_password():
    """ Modify user password.

        return:
            Modify the message password.
            modify password page.
    """
    update_password_form = UpdatePasswordForm()
    if request.method == 'POST' and update_password_form.validate_on_submit():
        user = UserInfo.query.filter_by(id=current_user.id).first()
        current_password = update_password_form.current_password.data
        if user.password == get_md5(current_password):
            user.password = get_md5(update_password_form.password.data)
            db.session.commit()
            flash(u'密码修改成功。')
            return redirect(url_for('site.base'))
        else:
            flash(u'当前密码输入错误。')

    return render_template('/user/update_password.html', form=update_password_form, user=current_user)


@users.route('/deleteuser/<int:user_id>/')
@login_required
def delete_user(user_id):
    """ Delete user information.

        Args:
            user_id: user identifier.

        return:
            user to delete the results.
    """
    try:
        print user_id ,type(user_id)
        print current_user.id, type(current_user.id)
        if user_id == current_user.id:
            flash(u'当前登陆用户为 %s,不能删除登陆账户' % current_user.username)
        else:
            query_user = UserInfo.query.filter_by(id=user_id)
            user_info = query_user.scalar()
            if user_info.username == 'admin':
                flash(u'超级管理员账户无法删除')
            else:
                query_user.delete()
                db.session.commit()
                flash(u'删除成功')
    except IntegrityError,e:
        flash(u'有用户、角色、或者权限信息由该用户创建，无法删除')
    return redirect(url_for('users.query_user'))
