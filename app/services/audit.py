#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-10-31"
from flask.ext.restful import Resource,fields,reqparse
from flask import Flask, request
from util.encrypt import md5
from util.ancc_spider import company_prefix_info
from util.file_util import base64_zip_filedata_to_save, remove_file
from app.models import AgentInfo,AuditRecord,FileInfo
from app import db
from sqlalchemy import and_
from datetime import *
import re
import uuid
parser = reqparse.RequestParser()
parser.add_argument('agent_name', type=str)
parser.add_argument('password', type=str)
parser.add_argument('domain_name', type=str,action='append')


class Audit(Resource):

    def get(self):

        response = {
            'code': '200',
            'msg': 'query ok!',
            'results': {}
        }
        args = parser.parse_args()
        agent_name = args['agent_name']
        md5_pw = md5(args['password'])
        domain_names = args['domain_name']
        print "parms =>>",agent_name,md5_pw,domain_names
        user = AgentInfo.query.filter(and_(AgentInfo.agent_name == agent_name, AgentInfo.password == md5_pw)).first()
        print user.agent_name, domain_names
        if user:
            for domain_name in domain_names:
                record = AuditRecord.query.filter(and_(AuditRecord.name == agent_name, AuditRecord.domain_name == domain_name)).scalar()
                response['results'][domain_name] = {}
                if record:
                    response['results'][domain_name]['audit_status'] = record.status
                    response['results'][domain_name]['audit_time'] = record.audit_time.strftime('%Y-%m-%d %H:%M:%S')
                    if record.status == '3':
                        response['results'][domain_name]['reason'] = record.audit_desc
        else:
            response['code'] = '201'
            response['msg'] = 'username or password id not correct!'
        return response

    def post(self):
        """
        data = {

            "agent_info":{
                "agent_name":'',
                "passwd":''                
            },
            "audit_data":{
                "bar_code":"",
                "biz_lic_image":{
                    "file_name":"",
                    "file_data":"",
                    
                },
                "bar_code_image":{
                    "file_name":"",
                    "file_data":""
                }
            
            }

        }
        :return:
        """
        print "in audit post"
        # print request.form['data']
        req = request.get_json(force=True)
        # print req
        rsp = {
            "code": '050',
            "msg": 'upload audit data ok!!!',
        }
        agent_info = req['agent_info']
        if agent_info:
            agent_name = agent_info['agent_name']
            passwd = md5(agent_info['passwd'])
        agent= AgentInfo.query.filter(and_(AgentInfo.agent_name == agent_name, AgentInfo.password == passwd)).first()
        if agent:
            print "auth ok"
            audit_data = req['audit_data']
            if audit_data:
                bar_code= audit_data['bar_code']

                if bar_code:
                    old_record = AuditRecord.query.filter(AuditRecord.domain_name == bar_code).scalar()
                    if old_record:
                        if old_record.status in ['0','1']:
                            rsp['code'] = "052"
                            rsp['msg'] = "the data is auditing"
                            return rsp
                        elif old_record.status == '2':
                            rsp['code'] = '053'
                            rsp['msg'] = 'the bar is already Review Successful'
                            return rsp
                    reg_code = re.findall(r'\d{13}', bar_code)
                    if reg_code:
                        r1 = company_prefix_info(reg_code[0][0:7])
                        r2 = company_prefix_info(reg_code[0][0:8])
                        if r1[0] == 0 and r2[0] == 0:
                            rsp['code'] = '055'
                            rsp['msg'] = 'Your bar-code can not search on http://www.ancc.org.cn'
                            return rsp
                            
                        if r1[0] == 2 or r2[0] == 2:
                            rsp['code'] = '056'
                            rsp['msg'] = 'Barcode not effective!'
                            return rsp

                    else:
                        rsp['code'] = '054'
                        rsp['msg'] = 'The barcode must 13 digital'
                        return rsp
                    biz_lic_image = {}
                    bar_code_image = {}
                    # print audit_data
                    if 'biz_lic_image' in audit_data:
                        biz_lic_image = audit_data['biz_lic_image']
                    if 'bar_code_image' in audit_data:
                        bar_code_image = audit_data['bar_code_image']
                        print bar_code_image['file_name']
                    # print bar_code_image
                    if (not bar_code_image) and (not biz_lic_image):
                        rsp['code'] = '057'
                        rsp['msg'] = "there has not tag 'bar_code_image' or 'bar_code_image' "
                        return rsp
                    else:

                        record = AuditRecord()
                        record.name = agent_name
                        record.domain_name = bar_code
                        record.status = '1'
                        record.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if old_record:
                            record .id = old_record.id
                            db.session.merge(record)
                        else:
                            db.session.add(record)
                            db.session.flush()

                        print ">>>>>>>>>>>>  ", record.id
                        if bar_code_image:
                            type = '04'
                            print "--------------------------------"
                            print type,record
                            bar_img_save_result = save_audit_image(bar_code_image, type, record)
                            if not bar_img_save_result:
                                rsp['code'] = '058'
                                rsp['msg'] = 'save bar_code_image failed'
                                return rsp

                        if biz_lic_image:
                            type = '03'
                            biz_img_save_result = save_audit_image(bar_code_image, type, record)
                            if not biz_img_save_result:
                                rsp['code'] = '058'
                                rsp['msg'] = 'save biz_lic_image failed'
                                return rsp
                        db.session.commit()
                else:
                    rsp['code'] = '059'
                    rsp['msg'] = 'the tag <bar_code> is null'

        else:
            rsp['code'] = '051'
            rsp['msg'] = 'username or password id not correct'
            return rsp
        return rsp

def save_audit_image(dict_data, type, record):
    """

    :param dict_data: {'file_name': str,'file_data':image_data}
    :param type:''
    :param record:
    :return:
    """
    try:
        file_name = dict_data['file_name']
        file_data = dict_data['file_data']
        f_info = FileInfo.query.filter(and_(FileInfo.ref_id == record.id, FileInfo.category == type)).scalar()
        print f_info
        if not f_info:
            f_info = FileInfo()
        else:
            remove_file(f_info.file_path)
        f_info.category = type
        f_info.ref_id = record.id
        filename = str(uuid.uuid4()) + file_name[file_name.rfind('.'):]
        result = base64_zip_filedata_to_save(filename, file_data, '01')
        print result
        if result[0] == 1:
            save_path = result[1]
            f_info.file_path = save_path
        db.session.merge(f_info)
        return True
    except Exception, e:
        return False