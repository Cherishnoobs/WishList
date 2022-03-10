# -*- coding: UTF-8 -*-
'''
@Description:  日志模块
'''


import logging
import os

debug = (os.getenv('mode','').lower() == 'debug')

log_level = logging.DEBUG if debug else logging.INFO
log_format = '%(asctime)s %(levelname)s %(name)s %(message)s'
log_date = '%H:%M:%S'  # '%m-%d %H:%M:%S'

logging.basicConfig(level=log_level,
                    format=log_format,
                    datefmt=log_date)

def get_logger(tag: str = '-'):
    return (logging.getLogger(tag))