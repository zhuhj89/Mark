# -*- coding: utf-8 -*-
"""
  the whois  interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-05"

from app.extensions import spyne
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.model.primitive import Unicode
from util.encrypt import md5
from util.public import get_domain_info, get_domain_status, get_contact_info, get_org_info,get_domain_host,get_all_contact_info
from app.models.user_info import UserInfo
from app.models.agent_info import AgentInfo
from app.models.whois_service_rsp import WhoisQueryRsp, DomainInfo,ContactInfo
from conf.config import get_domain_status_value,get_contact_type_value
from sqlalchemy import and_

class WhoisService(spyne.Service):
    __service_url_path__ = '/soap/whoisService'

    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()
    # __in_protocol__ = HttpRpc(validator='soft')
    # __out_protocol__ = JsonDocument(ignore_wrappers=True)

    @spyne.srpc(Unicode, Unicode, Unicode, _returns=WhoisQueryRsp)
    def whois_query(name, passwd, domain_name):
        rsp = WhoisQueryRsp()
        rsp.return_code = '070'
        rsp.return_msg = 'Whois Query Successed!!'
        md5_pw = md5(passwd)
        user = UserInfo.query.filter(and_(UserInfo.name == name, UserInfo.password == md5_pw)).scalar()
        print user
        if user:
            domain_info_result = get_domain_info(domain_name)
            print domain_info_result
            if domain_info_result[0] == 1:
                domain_info = domain_info_result[1]
                domain = DomainInfo()
                domain.name = domain_info.name
                domain.reg_date = domain_info.crdate
                domain.exp_date = domain_info.exdate

                registrar_id = domain_info.registrant
                registrar = AgentInfo.query.filter(AgentInfo.id == registrar_id).scalar()
                domain.registrar = registrar.comp_name

                contact_info = get_all_contact_info(domain_info.id, [1], [2])[1].first()
                domain.registrant = unicode(contact_info.name, 'utf8')
                domain.email = contact_info.email

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
                domain.status = ','.join(status)

                hosts = get_domain_host(domain_info.id)[1]
                name_server = []
                for host in hosts:
                    name_server.append(host.name)
                domain.name_server = ','.join(name_server)

                rsp.result = domain
            else:
                rsp.return_code = '071'
                rsp.return_msg = 'the search result is null'
                return rsp
        else:
            rsp.return_code = '059'
            rsp.return_msg = 'username or password id not correct!'
            return rsp
        print rsp
        return rsp




