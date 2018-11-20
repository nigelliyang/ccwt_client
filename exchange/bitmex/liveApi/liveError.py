#!/usr/bin/env python
# -*- coding: utf-8 -*-
from exchange.bitmex.liveApi import liveLogger

logger = liveLogger.getLiveLogger("Exception")

def ErrorShow(msg):
    logger.warning(msg)

