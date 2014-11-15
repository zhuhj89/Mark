# -*- coding: utf-8 -*-
"""
  the audit view moudle
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-27"
from conf.config import Page_Count
from flask import Blueprint, render_template,request,url_for,Module,redirect,flash
from app.models.file_info import FileInfo
from app.models.audit_record import AuditRecord
from app.models.audit_record_detail import AuditRecordDetail
from app.models.flow_link import FlowLink
from flask.ext.login import login_required
from util.public import get_domain_info, get_all_contact_info, get_contact_info ,get_org_info
from app import db
import os
import re
from sqlalchemy import and_
import datetime

audit = Blueprint('audit', __name__)
user_name = "zhangsan"

@audit.route('/test')
@login_required
def test():
    return render_template('base.html')

@audit.route('/query', methods=['GET', 'POST'])
@login_required
def query(domain_name='', type='' , page=1):

    if request.values.has_key('type'):
        type = request.values['type']
    if request.values.has_key('domain_name'):
        domain_name = request.values['domain_name'].strip()
    if request.values.has_key('page'):
        page = int(request.values['page'])
    print "type is %s" % type
    print "domain_name is %s" % domain_name
    print "page is %s" % page
    if type:
        if domain_name:
            print "domain_name is %s,type is %s" % (domain_name,type)
            page_url = lambda page: url_for('audit.query', type=type, domain_name=domain_name, page=page)
        else:
            print "type not null,domain null"
            page_url = lambda page: url_for('audit.query', type=type, page=page)

        record_list = AuditRecord.query.filter(and_(AuditRecord.status == type,AuditRecord.domain_name.like('%%%s%%' % domain_name))).\
            paginate(page, per_page=Page_Count)
    else:
        if domain_name:
            page_url = lambda page: url_for('audit.query', domain_name=domain_name, page=page)
        else:
            print "type and domain_name is all null"
            page_url = lambda page: url_for('audit.query', page=page)
        print "type is null"
        record_list = AuditRecord.query.filter(AuditRecord.domain_name.like('%%%s%%' % domain_name)).\
            paginate(page, per_page=Page_Count)

    print record_list.page
    print record_list.pages
    # return render_template('/audit/list.html')
    return render_template('/audit/list.html', domain_name=domain_name, type=type, records=record_list, page_url=page_url)


record_check = {

    'bussiness_lic': {'check1_1': ['营业执照是否过有效期？','营业执照已过有效期']},
    'code_certific': {'check2_1': ['条码证书是否过有效期？','条码证书已过有效期']}

}

@audit.route('/detail/<id>')
@login_required
def record_detail(id):
    record = AuditRecord.query.get(id)
    # if record:
    #     images = FileInfo.query.filter(and_(FileInfo.ref_id == record.id, FileInfo.category.in_(['03', '04']))).all()
    #     list_img = []
    #     for image in images:
    #         image.file_path = os.path.basename(image.file_path)
    #         # print image.file_path
    #         list_img.append(image)
    # domain_name = record.domain_name
    # domain_info = get_domain_info(domain_name)
    # contact_info = get_contact_info(domain_name)
    # org_info = get_org_info(domain_name)
    # return render_template('/audit/audit_record_detail.html', record=record, images=list_img,
    #                        domian_info=domain_info, contact_info=contact_info, org_info=org_info,
    #                        check=record_check)

    if record:
        return render_template('/audit/detail.html', record=record)

@audit.route('/confirm/<id>', methods=['GET', 'POST'])
@login_required
def confirm(id):
    username = 'zhangsan'
    record = AuditRecord.query.get(id)
    if request.method == 'GET':
        if record:
            images = FileInfo.query.filter(and_(FileInfo.ref_id == record.id, FileInfo.category.in_(['03', '04']))).all()
            list_img = []
            for image in images:
                image.file_path = os.path.basename(image.file_path)
                # print image.file_path
                list_img.append(image)
        print list_img
        img_path = lambda category: [image.file_path for image in list_img if image.category == category][0]

        print img_path('03')
        print img_path('04')
        domain_name = record.domain_name
        bar_code = re.findall(r'\d{13}', domain_name)[0]
        print domain_name,type(domain_name)
        domain_result = get_domain_info(domain_name)
        print domain_result
        if domain_result[0] == 1:
            domain_info = domain_result[1]
            period = (domain_info.exdate - domain_info.crdate).days/30
            contact_info = get_all_contact_info(domain_info.id, 1, 2)[1].fetchone()
            org = unicode(contact_info.org, 'utf8')
            area = unicode(contact_info.cc, 'utf8') + " " + unicode(contact_info.sp, 'utf8') + " " + unicode(contact_info.city, 'utf8')
            street1 = contact_info.street1
            street2 = contact_info.street2
            street3 = contact_info.street3
            if street1 is None:
                street1 = ''
            if street2 is None:
                street2 = ''
            if street3 is None:
                street3 = ''
            address = unicode(street1, 'utf8') + "," + unicode(street2, 'utf8') + "," + unicode(street3, 'utf8')
            post_code = contact_info.pc
            return render_template('/audit/confirm.html', bar_code=bar_code, period=period,img_path=img_path,
                                org=org, area=area, address=address, post_code=post_code)

    if request.method == 'POST':
        print "in post"
        data = {
            'bar_code': {'lable': u'商品条码', 'check': None, 'msg': None},
            'period': {'lable': u'服务时长', 'check': None, 'msg': None},
            'org': {'lable': u'条码所有者', 'check': None, 'msg': None},
            'area': {'lable': u'所属区域', 'check': None, 'msg': None},
            'address': {'lable': u'通讯地址', 'check': None, 'msg': None},
            'post_code': {'lable': u'邮编', 'check': None, 'msg': None},
            'b_lic': {'lable': u'营业执照', 'check': None, 'msg': None},
            'certific': {'lable': u'条码证书', 'check': None, 'msg': None},
        }
        post_keys = request.form.keys()
        print post_keys,request.form
        audit_suggest = []
        for (key, value) in data.items():
            msg_key = key + '_msg'
            if key in post_keys:
                value['check'] = request.form[key]
                value['msg'] = request.form[msg_key]
                if value['check'] == '0':
                    audit_suggest.append(value['lable'] + u'审核不通过,' + value['msg'])
        print audit_suggest
        if len(audit_suggest) == 0:
            record.status = '2'
        else:
            record.status = '3'

        record.audit_desc = ';'.join(audit_suggest)
        record.auditer = username
        record.audit_time = datetime.datetime.now()
        db.session.commit()
        flash(u'%s,审核完毕' % record.domain_name)
        return redirect(url_for('audit.query',))

@audit.route('/confirm', methods=['GET', 'POST'])
@login_required
def aduit_confirm():
    if request.method == 'POST':
        record_id = request.form['record_id']
        record = AuditRecord.query.filter(AuditRecord.id == record_id).scalar()
        record_detail = AuditRecordDetail.query.filter(and_(AuditRecordDetail.record_id == record_id,
                                                       AuditRecordDetail.status == '2')).scalar()
        record_detail.auditer = user_name

        print request.form['suggest']
        check_result = []
        for check in record_check:
            for check_item in record_check[check]:
                if request.form[check_item] == '1':
                    check_result.append(record_check[check][check_item][1])
        if check_result:
            record_detail.audit_desc = '审核未通过, ' + ','.join(check_result)
            record_detail.status = '4'
            record.status = '3'
        else:
            record_detail.audit_desc = '审核通过'
            record_detail.status = '3'
            record_detail.audit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            flow_link = FlowLink.query.filter(FlowLink.previous_node_id == record_detail.flow_node_id).scalar()
            if flow_link:
                next_detail = AuditRecordDetail.query.\
                    filter(and_(AuditRecordDetail.flow_node_id == flow_link.next_node_id,
                                AuditRecordDetail.record_id == record_id)).scalar()
                next_detail.status = '2'
            else:
                record.status = '2'
        db.session.commit()
        return record_detail.audit_desc
