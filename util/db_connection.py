# -*- coding: utf-8 -*-
'''connection DB'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf.config import __APPROVE_DB_CONFIG__ as approve_db
from conf.config import __EPP_SERVER_DB_CONFIG__ as  epp_server_db
from conf.config import __EPP_MS_DB_CONFIG__ as  epp_ms_db

# db_epp
base = declarative_base()
# appwove_db connection
conn_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?use_unicode=0&charset=utf8' % (approve_db['__DB_USER__'], approve_db['__DB_PWD__'], approve_db['__DB_HOST__'], approve_db['__DB_PORT__'], approve_db['__DB_NAME__'])
engine = create_engine(conn_url, echo=True)
session = sessionmaker(bind=engine)()



# epp server connection
epp_conn_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?use_unicode=0&charset=utf8' % (epp_server_db['__DB_USER__'], epp_server_db['__DB_PWD__'], epp_server_db['__DB_HOST__'], epp_server_db['__DB_PORT__'], epp_server_db['__DB_NAME__'])
epp_engine = create_engine(epp_conn_url, echo=True)
epp_session = sessionmaker(bind=epp_engine)()


# epp server connection
epp_ms_conn_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?use_unicode=0&charset=utf8' % (epp_ms_db['__DB_USER__'], epp_ms_db['__DB_PWD__'], epp_ms_db['__DB_HOST__'], epp_ms_db['__DB_PORT__'], epp_ms_db['__DB_NAME__'])
epp_ms_engine = create_engine(epp_ms_conn_url, echo=True)
epp_ms_session = sessionmaker(bind=epp_ms_engine)()

