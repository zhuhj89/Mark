# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-19"

__PRODUCT_POST_URL__ = 'http://183.63.152.235:81/routerjson/whois'

# db
__APPROVE_DB_CONFIG__ = {
    '__DB_HOST__': '127.0.0.1',
    '__DB_PORT__': 3306,
    '__DB_NAME__': 'approve_ws',
    '__DB_USER__': 'root',
    '__DB_PWD__': 'root'

}
__EPP_SERVER_DB_CONFIG__ = {
    '__DB_HOST__': '127.0.0.1',
    '__DB_PORT__': 3306,
    '__DB_NAME__': 'db_epp',
    '__DB_USER__': 'root',
    '__DB_PWD__': 'root'
}

__EPP_MS_DB_CONFIG__ = {
    '__DB_HOST__': '127.0.0.1',
    '__DB_PORT__': 3306,
    '__DB_NAME__': 'db_mark',
    '__DB_USER__': 'root',
    '__DB_PWD__': 'root'

}

__IMAGES_STATIC_PATH = './app/static/upload'


image_limit = {

    'type' : 'jpeg',
    'width': 1000,
    'higth':1000,
    'w_dpi_limit':100,
    'h_dpi_limit':100,
    'file_size' : 2*(1024*1024)
}

__DOMAINSTATUS = {
    '1': 'clientDeleteProhibited',
    '2': 'clientHold',
    '3': 'clientRenewProhibited',
    '4': 'clientTransferProhibited',
    '5': 'clientUpdateProhibited',
    '6': 'inactive',
    '7': 'ok',
    '8': 'pendingCreate',
    '9': 'pendingDelete',
    '10': 'pendingRenew',
    '11': 'pendingTransfer',
    '12': 'pendingUpdate',
    '13': 'serverDeleteProhibited',
    '14': 'serverHold',
    '15': 'serverRenewProhibited',
    '16': 'serverTransferProhibited',
    '17': 'serverUpdateProhibited'
}


def get_domain_status_value(key):
    return __DOMAINSTATUS[key]

# Operating domain contact type.
__CONTACT_TYPE = {
      '1': 'admin',
      '2': 'billing',
      '3': 'tech',
}


def get_contact_type_value(key):
    return __CONTACT_TYPE[key]


# Contact postal address writing type.
# 'int' internationalization. 'loc' localization.
__CONTACT_POSTAL_TYPE = {
        '1': 'int',
        '2': 'loc'
}


def get_contact_postal_type_value(key):
    return __CONTACT_POSTAL_TYPE[key]
