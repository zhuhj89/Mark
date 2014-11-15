# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-25"

from app.extensions import db,spyne
from flask.ext.spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode
from spyne.model.binary import ByteArray
from app.models.file_info import FileInfo, add_file
from app.models.audit_record import AuditRecord, add_audit_record,get_record_by_domain_status
from app.models.flow import Flow
from app.models.flow_node import FlowNode
from app.models.flow_link import FlowLink
from app.models.audit_record_detail import AuditRecordDetail
from app.models import AgentInfo
from util.file_util import save_file
from util.ancc_spider import company_prefix_info
from util.encrypt import md5
from app.models.audit_sercice_rsp import UploadDataRsp, QueryDomainStatRsp
from util.db_connection import epp_ms_session
from sqlalchemy import and_
import uuid
import datetime
import re


class AuditService(spyne.Service):
    __service_url_path__ = '/soap/auditService'

    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Unicode, Unicode, ByteArray(min_occurs=1, nullable=False), ByteArray(min_occurs=1, nullable=False), _returns=UploadDataRsp)
    def upload_data(name, passwd, domain_name, business_lic_imgdata, code_certific_imgdata):
        rsp = UploadDataRsp()
        rsp.code = '050'
        rsp.msg = 'ok,information upload succeed!'   #
        record = get_record_by_domain_status(domain_name, '1')
        print record
        print '--'*50
        if record:
            rsp.code = '057'
            rsp.msg = 'this domain has not approved record!'  #
            return rsp
        md5_pw = md5(passwd)
        # user = epp_ms_session.execute('select * from agent_info  where agent_name=:agent_name and password=:password', {'agent_name': name, 'password': md5_pw}).first()
        user = AgentInfo.query.filter(and_(AgentInfo.agent_name == name, AgentInfo.password == md5_pw)).first()
        print user.agent_name
        if user:
            bar_code = re.findall(r'\d{13}', domain_name)
            print bar_code
            if bar_code:
                r1 = company_prefix_info(bar_code[0][0:7])
                r2 = company_prefix_info(bar_code[0][0:8])

                if r1 or r2:
                    if r1:
                        if r1['status'] == '0':
                            rsp.code = '055'
                            rsp.msg = 'Barcode not effective!'
                            return rsp
                    else:
                        if r2['status'] == '0':
                            rsp.code = '055'
                            rsp.msg = 'Barcode not effective!'
                            return rsp
                else:
                    rsp.code = '056'
                    rsp.msg = "Your bar-code cant't seacrch on http://www.ancc.org.cn"
                    return rsp
            else:
                rsp.code = '054'
                rsp.msg = 'The domain name must include 13 digital barcode!'
                return rsp

            audit_recode = AuditRecord()
            audit_recode.name = name
            audit_recode.domain_name = domain_name
            audit_recode.status = '1'
            audit_recode.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # add a audit record
            pk_id = add_audit_record(audit_recode)
            if pk_id:

                # save bussiness_lic
                lic_path = save_file(str(uuid.uuid1())+'.jpg', business_lic_imgdata,'01')
                lic_image = FileInfo()
                lic_image.ref_id = pk_id
                lic_image.category = '03'
                lic_image.file_path = lic_path
                lic_pk_id = add_file(lic_image)

                # save certific image
                if lic_pk_id:
                    code_certific_path = save_file(str(uuid.uuid1())+'.jpg',code_certific_imgdata,'01')
                    certfic_image = FileInfo()
                    certfic_image.file_path = code_certific_path
                    certfic_image.category = '04'
                    certfic_image.ref_id = pk_id
                    cerf_pk_id = add_file(certfic_image)
                    if cerf_pk_id:
                        pass
                    #     audit_record_init(pk_id)

                    else:
                        rsp.code = '053'
                        rsp.msg = 'Save the  code certificate  failed'
                        return rsp
                else:
                    rsp.code = '052'
                    rsp.msg = 'Save the bussiness  license failed'
                    return rsp
            else:

                rsp.code = '051'
                rsp.msg = 'Create the record of rudit failed'
                return rsp
        else:
            rsp.code = '059'
            rsp.msg = 'username or password id not correct!'
            return rsp
        return rsp
    @spyne.srpc(Unicode, Unicode, Unicode, _returns=QueryDomainStatRsp)
    def query_audit_status(name, passwd, domain_name):
        rsp = QueryDomainStatRsp()
        rsp.code = '060'
        rsp.msg = 'Query status Successed!!'   #
        md5_pw = md5(passwd)
        user = epp_ms_session.execute('select * from agent_info  where agent_name=:agent_name and password=:password', {'agent_name': name, 'password': md5_pw}).first()
        print user.agent_name,domain_name
        if user:
            record = AuditRecord.query.filter(and_(AuditRecord.name == name, AuditRecord.domain_name == domain_name)).scalar()
            if record:
                rsp.domain_name = record.domain_name
                rsp.audit_status = record.status
                rsp.audit_time = record.audit_time
                if record.status == '3':
                    rsp.reason = record.audit_desc
                print rsp.reason
            else:
                rsp.code = '061'
                rsp.msg = 'there has no aduit record of %s' % (domain_name,)
        else:
            rsp.code = '059'
            rsp.msg = 'username or password id not correct!'
            return rsp
        return rsp
def audit_record_init(record_id):
    flow = Flow.query.filter(Flow.flow_code == '001').scalar()
    flow_id = flow.flow_id
    flow_nodes = FlowNode.query.filter(FlowNode.flow_id == flow_id).all()
    start_node = None
    for flow_node in flow_nodes:
        record_detail = AuditRecordDetail()
        record_detail.flow_node_id = flow_node.flow_node_id
        record_detail.record_id = record_id

        if flow_node.flag == '1':
            record_detail.status = '3'
            start_node = flow_node
        else:
            record_detail.status = '1'
        db.session.add(record_detail)
    db.session.commit()
    next_nodes = FlowLink.query.\
        filter(and_(FlowLink.previous_node_id == start_node.flow_node_id, FlowLink.flow_id == flow_id)).all()
    print next_nodes
    for next_node in next_nodes:
        record_detail = AuditRecordDetail.query.\
            filter(and_(AuditRecordDetail.flow_node_id == next_node.next_node_id,\
                        AuditRecordDetail.record_id == record_id)).scalar()
        record_detail.status = '2'
        db.session.merge(record_detail)
    db.session.commit()

    return True



