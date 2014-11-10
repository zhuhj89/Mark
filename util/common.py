# -*- coding: utf-8 -*-
""" Public function declaration."""
__author__ = "Wangchuang"
__email__ = "wangchuang@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-20 10:20:36"


import hashlib


def get_md5(readable_str):
	""" md5 encrypted string.

		Args:
			readable_str: Need to encrypt a string.

		return: Encrypted string.

	"""
	return hashlib.md5(readable_str).hexdigest()

