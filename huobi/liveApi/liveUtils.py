from pyalgotrade.utils import dt
from datetime import datetime
import time
import pytz

localTz = pytz.timezone('Asia/Shanghai')


def timestamp():
    return int(time.time())


def utcnow():
    return dt.as_utc(datetime.utcnow())


def timestamp_to_DateTimeLocal(timestamp):
    return datetime.fromtimestamp(timestamp, localTz)


def localTime():
    return timestamp_to_DateTimeLocal(timestamp())


def utcToLocal(utcDatetime):
    return timestamp_to_DateTimeLocal(dt.datetime_to_timestamp(utcDatetime))


def RoundDown(f, n):
    r = round(f, n)
    return r if r <= f else r - (10 ** -n)


def PriceRound(price):
    return RoundDown(price, 2)


def CoinRound(coin):
    return RoundDown(coin, 4)


import traceback
from liveApi import liveError


def tryForever(func):
    def forever(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                liveError.ErrorShow('traceback:%s' % traceback.format_exc())
                liveError.ErrorShow('%s => %s' % (func.__name__, e))
                time.sleep(1)
                continue

    return forever


'''
_eDict = {}
def exceDebug(fn):
    _eDict[fn] = True
    def waper(*args, **kwargs):
        __a = _eDict[fn]
        _eDict[fn] = not __a
        if __a is True:
            raise Exception('Debug:%s'%fn.__name__)
        print('')
        print('')
        print('==========success :: %s'%fn.__name__)
        print('')
        print('')
        return fn(*args, **kwargs)
    return waper
'''
