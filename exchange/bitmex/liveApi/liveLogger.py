#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from pyalgotrade import logger

from exchange.bitmex.liveApi import liveUtils

log_format = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
level = logging.INFO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# print(BASE_DIR)
log_dir = os.path.join(BASE_DIR, 'logs')
_file = 'info.log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)  # 判断路径是否存在，不存在则创建路径
file_log = os.path.join(log_dir, _file)


fileHandler = None


class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return "[%s]" % liveUtils.localTime()


def initLogger(logger):
    global fileHandler
    if fileHandler is None:
        fileHandler = logging.FileHandler(file_log)
        fileHandler.setFormatter(log_format)
        fileHandler.setFormatter(Formatter(log_format))
    logger.addHandler(fileHandler)


def getLiveLogger(name):
    log = logger.getLogger(name)
    initLogger(log)
    return log
