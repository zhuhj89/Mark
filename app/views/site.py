#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-11-05"

from flask import Blueprint, redirect, url_for, render_template
site = Blueprint("site", __name__)
@site.route('/')
def index():
    """ Default page.

        return:
            default page.
    """
    return redirect(url_for('users.login'))


@site.route('base')
def base():
    """ Default page.

        return:
            default page.
    """
    return render_template('/base.html')
    # return "okkkk"