#!/usr/bin/env python
# -*- coding: utf-8 -*-
from exchange.bitmex.liveApi import liveLogger
import pyalgotrade.logger as log
# logger = liveLogger.getLiveLogger("Exception")
logger = log.getLogger("Exception")

def ErrorShow(msg):
    logger.warning(msg)

