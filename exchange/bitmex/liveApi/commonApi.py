#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

from exchange.bitmex.bitmex_sdk import ApiClient
from exchange.bitmex.bitmex_client import BitmexTradeClient
# from exchange.bitmex.liveApi import liveLogger
import pyalgotrade.logger as log
from exchange.bitmex.liveApi.liveUtils import *

# logger = liveLogger.getLiveLogger("K-Line")
logger = log.getLogger("K-line")
# client = ApiClient('API_KEY', 'API_SECRET')

def getKLineBar(identifier, precision, period, length=1):
    logger.info('getKLine:%s %s %s %s' % (identifier, precision, period, length))
    # length = length + 1 if length < 10 else 10
    length = 5
    client = BitmexTradeClient(identifier)

    # klines = client.mget('/market/history/kline', symbol=identifier.getSymbol(), period='%dmin' % period, size=length)
    klines = client.get_kline(identifier.getSymbol(), **{'binSize': precision, 'count': length})
    logger.info("klines: {}".format(klines))
    return klines
