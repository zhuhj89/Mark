#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" webservice server
"""
__author__ = "XiaoQian"
__email__ = "xiaoqian@cnnic.cn"
__copyright__ = "Copyright 2007, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-18 10:22:57"
import os
from tempfile import mkstemp
from soaplib.serializers.binary import Attachment
from soaplib.serializers.primitive import String
from soaplib.service import soapmethod
from soaplib.wsgi_soap import SimpleWSGISoapApp


class NiotWebService(SimpleWSGISoapApp):
    @soapmethod(String, _returns=String)
    def simple_method(self, param1):
        return 'param1= %s' % param1

    @soapmethod(Attachment, _returns=String)
    def file_upload(self, document):
        """
        This method accepts an Attachment object, and returns
        the filename of the archived file
        """
        fd, fname = mkstemp()
        os.close(fd)

        document.fileName = fname
        document.save_to_file()

        return fname

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        server = make_server('localhost', 7777, NiotWebService())
        server.serve_forever()
    except ImportError:
        print "Error: example server code requires Python >= 2.5"