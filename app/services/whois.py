#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhuhuijie'
__email__ = "zhuhuijie@cnnic.cn"
__copyright__ = "Copyright 2014,Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-10-30"


from flask.ext.restful import Resource,fields,reqparse
from flask import request
from util.encrypt import md5
from util.public import get_domain_info, get_domain_status, get_contact_info, get_org_info,get_domain_host,get_all_contact_info
from app.models.user_info import UserInfo
from app.models.agent_info import AgentInfo
from conf.config import get_domain_status_value,get_contact_type_value
from sqlalchemy import and_
from datetime import *
parser = reqparse.RequestParser()
parser.add_argument('domain_name', type=str)
class Whois(Resource):

    def get(self):
        args = parser.parse_args()

        rsp = {
            'code': '200',
            'msg': 'upload ok!!!',
            'data': {}
        }

        # md5_pw = md5(passwd)
        # user = UserInfo.query.filter(and_(UserInfo.name == name, UserInfo.password == md5_pw)).scalar()
        # print user
        # if user:
        domain_name = args['domain_name']
        domain_info_result = get_domain_info(domain_name)
        print domain_info_result
        if domain_info_result[0] == 1:
            domain_info = domain_info_result[1]
            info = {}
            info['name'] = domain_info.name
            info['reg_date'] = domain_info.crdate.strftime('%Y-%m-%d %H:%M:%S')
            info['exp_date'] = domain_info.exdate.strftime('%Y-%m-%d %H:%M:%S')

            registrar_id = domain_info.registrant
            print "registrar_id>>",registrar_id
            registrar = AgentInfo.query.filter(AgentInfo.id == registrar_id).scalar()
            info['registrar'] = registrar.comp_name

            contact_info = get_all_contact_info(domain_info.id, [1], [2])[1].first()
            info['registrant'] = unicode(contact_info.name, 'utf8')
            info['email'] = contact_info.email

            # domain.contacts = []
            # contact_infos = get_all_contact_info(domain_info.id, [1], [2])[1]
            # print contact_infos
            # for contact_info in contact_infos:
            #     print contact_info
            #     contact = ContactInfo()
            #     contact.type = get_contact_type_value(str(contact_info.contact_role))
            #     contact.registrant = unicode(contact_info.name, 'utf8')
            #     contact.email = contact_info.email
            #     domain.contacts.append(contact)

            status = []
            domian_status = get_domain_status(domain_info.id)[1]
            for item in domian_status:
                status.append(get_domain_status_value(str(item.status)))
            info['status'] = ','.join(status)

            hosts = get_domain_host(domain_info.id)[1]
            name_server = []
            for host in hosts:
                name_server.append(host.name)
            info['name_server'] = ','.join(name_server)

            rsp['data'] = info
        else:
            rsp['code'] = '071'
            rsp['msg'] = 'the search result is null'
        print rsp
        return rsp

