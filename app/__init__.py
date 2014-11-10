#coding=utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import restful

mark_app = Flask(__name__)
mark_app.config.from_object('config')
db = SQLAlchemy(mark_app)
api =restful.Api(mark_app)

import services.product_service
import services.audit_service
import services.whois_service
from app import views
from app.views import audit, flow, users,site
from app.services import Product, Whois, Audit

DEFAULT_MODULES = {

    'web_modules': [
        (site, "/"),
        (users, "/users"),
        (audit, "/audit"),
        (flow, "/admin"),

    ],
    'service_moudles': [
        (Product, '/api/product'),
        (Whois, '/api/whois'),
        (Audit, '/api/audit'),
    ]

}


def configure_modules(app, moudles):

    if 'web_modules' in moudles:

        for module, url_prefix in moudles['web_modules']:
            app.register_blueprint(module, url_prefix=url_prefix)
    if 'service_moudles' in moudles:
        for module, url_prefix in moudles['service_moudles']:
            api.add_resource(module, url_prefix)


configure_modules(mark_app, DEFAULT_MODULES)