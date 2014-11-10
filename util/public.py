# -*- coding: utf-8 -*-
"""
  the audit view moudle
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-09-04"

from util.db_connection import epp_session


def get_org_info(domain_name):
    domain_info = epp_session.execute('SELECT * FROM contact_postal_info WHERE  contact_id = ' +
                                      '(SELECT contact_id FROM domain_contact_info WHERE domain_id = ' +
                                      '(SELECT id FROM domain_info WHERE name =:domain_name))',
                                      {
                                      'domain_name': domain_name
                                      }).first()

    if domain_info:
        return [1, domain_info]
    else:
        return [0, None]


def get_contact_info(domain_name):
    contact_info = epp_session.execute('SELECT * FROM contact_info WHERE id = ' +
                                       '(SELECT contact_id FROM domain_contact_info WHERE domain_id = ' +
                                       '(SELECT id FROM domain_info WHERE name =:domain_name))',
                                       {
                                       'domain_name': domain_name
                                       }).first()

    if contact_info:
        return [1, contact_info]
    else:
        return [0, None]


def get_domain_host(domain_id):
    hosts = epp_session.execute('SELECT * FROM host_info WHERE id IN ' +
                                '(SELECT host_id FROM domain_host_info WHERE domain_id =:domain_id)',
                                {
                                'domain_id': domain_id
                                })
    if hosts:
        return [1, hosts]
    else:
        return [0, None]


def get_all_contact_info(domain_id, contact_role, language):
    domains = epp_session.execute('select * from domain_info')
    print domains
  #  contact_role = tuple(contact_role)
  #  language = tuple(language)
    contact_infos = epp_session.execute('SELECT c.email,c.voice,c.voice_x ,c.crdate,d.* FROM contact_info c ' +
                                        'RIGHT JOIN '
                                        '(SELECT a.domain_id,a.contact_id ,a.type AS contact_role, '
                                        'b.type AS language,b.name,b.org, b.cc, b.sp, b.city,'
                                        ' b.street1, b.street2, b.street3,b.pc ' +
                                        'FROM domain_contact_info a ' +
                                        'LEFT JOIN contact_postal_info b ON a.contact_id = b.contact_id) d ' +
                                        'ON c.id = d.contact_id WHERE d.domain_id =:domain_id ' +
                                        'and d.contact_role =:contact_role and d.language =:language',
                                        {
                                        'domain_id': domain_id,
                                        'contact_role': contact_role,
                                        'language': language
                                        }
                                        )
    if contact_infos:
        return [1, contact_infos]
    else:
        return [0, None]



def get_domain_info(domain_name):
    domain_info = epp_session.execute('select * from domain_info where name=:domain_name',
                                      {
                                      'domain_name': domain_name
                                      }).first()

    if domain_info:
        return [1, domain_info]
    else:
        return [0, None]


def get_domain_status(domain_id):

    domain_status = epp_session.execute('SELECT * FROM domain_status_info WHERE domain_id =:domain_id',
                                        {
                                        'domain_id': domain_id
                                        })
    if domain_status:
        return [1, domain_status]
    else:
        return [0, None]

