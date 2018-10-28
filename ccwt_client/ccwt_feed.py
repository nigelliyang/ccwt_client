#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/10/27 17:18    @Author  : xycfree
# @Descript: 

from ccwt_client.core import cli
from pyalgotrade.barfeed import membf, Frequency

from pyalgotrade.barfeed import dbfeed
from pyalgotrade.barfeed import membf
from pyalgotrade import bar
from pyalgotrade.utils import dt

def normalize_instrument(instrument):
    return instrument.upper()


# mongo DB.
# Timestamps are stored in UTC.
class Database(dbfeed.Database):

    def __init__(self):
        pass

    def getBars(self, instrument, frequency, timezone=None, fromDateTime=None, toDateTime=None):
        """
        :param instrument: exchange_symbol
        :param frequency: 频率
        :param timezone:
        :param fromDateTime:
        :param toDateTime:
        :return:
        """
        volume = None
        period, ticker_flag = self.get_frequency_info(frequency)
        if ticker_flag:
            colName = instrument + '_ticker'
            volume = 'base_volume'
        else:
            # 需要验证kline是否有数据

            # colName = instrument + '_kline_' + period
            # if colName not in self.__dataBase.collection_names():
            #     raise NotImplementedError()


            volume = 'volume'

        # client获取数据
        # col = self.__dataBase.get_collection(colName)

        col = get_data_info(instrument, period, ticker_flag, fromDateTime, toDateTime)

        ret = []
        map = {}
        for row in col:
            dateTime = dt.timestamp_to_datetime(row['time_stamp'] // 1000)
            if timezone:
                dateTime = dt.localize(dateTime, timezone)
            strDateTime =dateTime.strftime("%Y-%m-%d %H:%M:%S")
            if strDateTime not in map:
                ret.append(bar.BasicBar(dateTime, row['open'], row['high'], row['low'], row['close'], row[volume], None, frequency))
                map[strDateTime] = '1'
        print("===========ret: {}==========".format(ret))
        return ret


    def get_frequency_info(self, frequency):
        """获取高频数据"""
        period = ''
        ticker_flag = False

        if frequency == bar.Frequency.MINUTE:
            period = '1m'
        elif frequency == bar.Frequency.HOUR:
            period = '1h'
        elif frequency == bar.Frequency.DAY:
            period = '1d'
        elif frequency == bar.Frequency.WEEK:
            period = '1w'
        elif frequency == bar.Frequency.MONTH:
            period = '1M'
        elif frequency == bar.Frequency.SECOND:
            ticker_flag = True
        else:
            raise NotImplementedError()
        return period, ticker_flag


def get_data_info(instrument, period='', ticker_flag=False, fromDateTime='', toDateTime='', **kwargs):
    """ 获取kline/ticker数据
    :param toDateTime: 截止日期
    :param fromDateTime: 开始日期
    :param instrument: exchange_symbol
    :param period: kline
    :param ticker_flag: ticker
    :param kwargs:
    :return:
    """

    param = {
        'exchange': instrument.split('_')[0], 'symbol': instrument.split('_')[-1],  'start_date': fromDateTime,
        'end_date': toDateTime
    }

    if period:
        _method = 'kline'
        param['time_frame'] = period
        res = cli.kline(**param)
    else:
        _method = 'ticker'
        res = cli.ticker(**param)

    if res and isinstance(res, list):
        _keys = [k for k in res[0].keys() if _method in k]
        datas = res[0].get(_keys[0])
        return datas
    else:
        raise NotImplementedError()



class Feed(membf.BarFeed):
    def __init__(self, frequency, dbConfig=None, maxLen=None):
        super(Feed, self).__init__(frequency, maxLen)
        self.db = Database()

    def barsHaveAdjClose(self):
        return False

    def loadBars(self, instrument, timezone=None, fromDateTime=None, toDateTime=None):
        bars = self.db.getBars(instrument, self.getFrequency(), timezone, fromDateTime, toDateTime)
        self.addBarsFromSequence(instrument, bars)


if __name__ == '__main__':
    feed = Feed(bar.Frequency.MINUTE)
    feed.loadBars("binance_ADABTC")

