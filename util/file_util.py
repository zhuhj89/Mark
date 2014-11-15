# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-20"
import sys,os
import ConfigParser
import Image
import conf.config as config
from spyne.error import ValidationError
import base64
import zlib
def read_config(config_file_path, field, key):

    print config_file_path
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)

    except:
        sys.exit(1)
    return result


def save_file(file_name,file_data,type):
    """

    :param file_name:
    :param file_data:
    :param type: 01- 'aduit' 02-product
    :return:
    """
    static_path = config.__IMAGES_STATIC_PATH
    if type == '01':

        static_path = static_path + '/audit'

    elif type == '02':
        static_path = static_path + '/product'

    path = os.path.join(static_path, file_name)

    f = open(path,'wb')

    for data in file_data:
        f.write(data)
    f.close()

    return path


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    else:
        return False


def file_zip_base64(file_name):
    try:
        with open(file_name,'rb') as f:
            data =base64.b64encode(zlib.compress(f.read()))
            f.close()
        return [1, data]
    except Exception, e:
        return [0, e]

def base64_zip_filedata_to_save(file_name,file_data,type):

    try:
        data = zlib.decompress(base64.b64decode(file_data))
        file_path = save_file(file_name, data, type)
        return [1, file_path]
    except Exception, e:
        return [0, e]


def get_file_data(file_path):
    file_name = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        fdata = f.read()
        # # fdata = base64.b64encode(f.read())
        # print type(fdata)
        f.close()
        import base64, zlib
        # print fdata
        fdata = base64.b64encode(zlib.compress(fdata))
        print fdata
    return [file_name, fdata]


def get_image_info(image_path):
    image = Image.open(image_path)
    info = {}
    info['type'] = image.format
    info['image_size'] = image.size
    if 'dpi' in image.info.keys():
        info['dpi'] = image.info['dpi']
    info['file_size'] = os.path.getsize(image_path)

    return info