#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from pyalgotrade import logger

from exchange.bitmex.liveApi import liveUtils

log_format = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
level = logging.INFO
log_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(log_dir)
file_log = os.path.join(log_dir, 'logs/info.log')

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
