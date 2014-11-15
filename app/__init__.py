#coding=utf-8

from flask import Flask,abort
from extensions import db,login_manager
from flask.ext import restful
from app.views import audit, flow, users,site,agent,auth,role_auth,role
from app.services import Product, Whois, Audit
import logging
from util.logger import logfile
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler
DEFAULT_APP_NAME = 'app'
DEFAULT_MODULES = {

    'web_modules': [
        (site, "/"),
        (users, "/users"),
        (audit, "/audit"),
        (flow, "/admin"),
        (agent, "/agent"),
        (auth, "/auth"),
        (role, "/role"),
        (role_auth, "/roleauth"),

    ],
    'service_moudles': [
        (Product, '/api/product'),
        (Whois, '/api/whois'),
        (Audit, '/api/audit'),
    ]

}


def create_app(config=None):
    app = Flask(DEFAULT_APP_NAME)
    api = restful.Api(app)
    app.config.from_object(config)
    configure_extensions(app)
    configure_modules(app, api, DEFAULT_MODULES)
    # configure_logging(app)
    return app


def configure_modules(app, api, moudles):

    if 'web_modules' in moudles:

        for module, url_prefix in moudles['web_modules']:
            app.register_blueprint(module, url_prefix=url_prefix)
    if 'service_moudles' in moudles:
        for module, url_prefix in moudles['service_moudles']:
            api.add_resource(module, url_prefix)

def configure_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    @app.after_request
    def after_request(response):
        try:
            db.session.commit()

        except Exception,e:

            db.session.rollback()
            abort(500)
        return response

def configure_logging(app):
    loggers = [app.logger]
    for logger in loggers:
        file_handler = TimedRotatingFileHandler("mark", when='S', interval=1, backupCount=40)
        file_handler.suffix = "%Y%m%d.log"
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)