#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/10/27 17:18    @Author  : xycfree
# @Descript: 
from ccwt_client import logger
import datetime
from ccwt_client.core import cli
from pyalgotrade.barfeed import dbfeed
from pyalgotrade.barfeed import membf
from pyalgotrade import bar
from pyalgotrade.utils import dt

log = logger.getLogger("ccwt_feed")

def normalize_instrument(instrument):
    return instrument.upper()


# mongo DB.
# Timestamps are stored in UTC.
class Database(dbfeed.Database):

    def __init__(self):
        pass

    def getBars(self, instrument, frequency, test_back=True, timezone='', start_date='', end_data=''):
        """  frequency 为 bar.Frequency.SECOND时获取ticker数据，其他的获取kline数据；
        :param instrument: exchange_symbol
        :param frequency: 频率
        :param timezone:
        :param start_date:
        :param end_data:
        :return:
        """
        period, ticker_flag = self.get_frequency_info(frequency)
        volume = 'base_volume' if ticker_flag else 'volume'
        limit = 100 if test_back else ''
        # client获取数据
        col = get_data_info(instrument, period, ticker_flag, start_date, end_data, limit)

        _tmp = []
        ret = []
        map = {}
        for row in col:

            # _time_stamp = row.get('time_stamp', '') or row.get('timestamp', '')
            # log.info("==========_time_stamp: {}==========".format(_time_stamp))
            # dateTime, strDateTime = self.get_time_stamp_info(_time_stamp, timezone)

            # log.info('dateTime: {}, strDateTime: {}'.format(dateTime, strDateTime))
            dateTime = row.get('sys_time')
            try:
                if dateTime not in map:
                    # print("open: {}, preclose: {}".format(row.get('open', 0), row.get('preclose', 0)))
                    ret.append(
                        bar.BasicBar(dateTime, row.get('open', 0) or row.get('preclose', 0), row.get('high', 0), row.get('low', 0),
                                     row.get('close', 0), row[volume], None, frequency))
                    map[dateTime] = '1'
                    _tmp.append(
                            [dateTime, row.get('open', 0) or row.get('preclose', 0), row.get('high', 0), row.get('low', 0),
                             row.get('close', 0), row[volume], None, frequency])
            except Exception as e:
                log.warning("异常: {}".format(e))
                pass

        log.debug("======ret is len: {}======".format(len(ret)))
        log.debug("=========_tmp top 3: {}============".format(_tmp[:3]))
        return ret

    def get_time_stamp_info(self, time_stamp, timezone=''):
        """ time_stamp转换为datetime
        :param time_stamp:
        :return:
        """
        try:
            dateTime = dt.timestamp_to_datetime(time_stamp // 1000)
            if timezone:
                dateTime = dt.localize(dateTime, timezone)
            strDateTime = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            log.debug("时间戳转换失败: {}".format(e))
            try:
                dateTime = datetime.datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%S")
            except:
                dateTime = datetime.datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            strDateTime = dateTime.strftime("%Y-%m-%d %H:%M:%S")
            # dateTime = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        return dateTime, strDateTime


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


def get_data_info(instrument, period='', ticker_flag=False, start_date='', end_date='', limit='', **kwargs):
    """ 获取kline/ticker数据
    :param end_date: 截止日期
    :param start_date: 开始日期
    :param instrument: exchange_symbol
    :param period: kline
    :param ticker_flag: ticker
    :param kwargs:
    :return:
    """

    param = {
        'exchange': instrument.split('_')[0], 'symbol': instrument.split('_')[-1], 'start_date': start_date,
        'end_date': end_date, 'limit': limit
    }

    if period:
        _method = 'kline'
        param['time_frame'] = period
        res = cli.kline(**param)
    elif ticker_flag:
        _method = 'ticker'
        res = cli.ticker(**param)
    else:
        raise NotImplementedError()

    if res and isinstance(res, list):
        _keys = [k for k in res[0].keys() if _method in k]
        datas = res[0].get(_keys[0])
        log.info('Get data info is top 3: {}'.format(datas[:3]))
        return datas
    else:
        raise NotImplementedError()


class Feed(membf.BarFeed):
    def __init__(self, frequency, dbConfig=None, maxLen=None):
        super(Feed, self).__init__(frequency, maxLen)
        self.db = Database()

    def barsHaveAdjClose(self):
        return False

    def loadBars(self, instrument, test_back, timezone='', start_date='', end_date=''):
        """  获取交易所ticker/kline数据
        :param instrument:
        :param test_back: 回测标识，TRUE: 表示回测，默认返回1000条数据， False: 获取时间段区间数据
        :param timezone: 时区
        :param start_date: 开始日期 与系统时间相比，不与交易所时间比较
        :param end_date: 截止日期 与系统时间相比，不与交易所时间比较
        :return:
        """
        if not test_back:
            if not start_date and not end_date:
                raise
        log.info("instrument: {}.".format(instrument))
        bars = self.db.getBars(instrument, self.getFrequency(), test_back,  timezone, start_date, end_date)
        self.addBarsFromSequence(instrument, bars)


if __name__ == '__main__':
    feed = Feed(bar.Frequency.SECOND)
    # feed.loadBars("bitmex_LTCZ18")  # bitmex_XBTUSD  binance_ADABTC  okex_LIGHTBTC
    feed.loadBars("okex_LIGHTBTC")  # bitmex_XBTUSD  binance_ADABTC  okex_LIGHTBTC
