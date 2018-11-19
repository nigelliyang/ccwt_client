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
from exchange.bitmex.liveApi import liveLogger
from exchange.bitmex.liveApi.liveUtils import *

logger = liveLogger.getLiveLogger("K-Line")

client = ApiClient('API_KEY', 'API_SECRET')


def getKLineBar(identifier, endTimestamp, period, length=1):
    logger.info('getKLine:%s %s %s %s' % (identifier, endTimestamp, period, length))
    length = length + 1 if length < 1000 else 1000

    klines = client.mget('/market/history/kline', symbol=identifier.getSymbol(), period='%dmin' % period, size=length)
    if len(klines) != length:
        return None
    if timestamp() - endTimestamp > period * 60 + 30 and length < 100:
        del klines[1]
    else:
        del klines[0]
    x = klines[0]
    f = timestamp_to_DateTimeLocal
    logger.info('cur: %s recv: %s ecpect: %s eq: %s' % (f(timestamp()), f(x.id), f(endTimestamp), endTimestamp == x.id))
    if x.id < endTimestamp:
        return None
    if x.id > endTimestamp:
        klines[0].id = endTimestamp
        logger.info('fuck!')

    return [{
        "Timestamp": k.id,
        "Open": k.open,
        "High": k.high,
        "Low": k.low,
        "Close": k.close,
        "Volume": k.vol,
    }
        for k in klines
    ]
