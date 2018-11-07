#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/11/6 22:44 By xycfree
# @Descript:

from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
from pyalgotrade.barfeed.csvfeed import GenericBarFeed
from pyalgotrade.stratanalyzer import returns, sharpe
from pyalgotrade.utils import stats

from ccwt_client.ccwt_feed import Feed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi

# 构建一个策略
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, instrument_1=''):
        super(MyStrategy, self).__init__(feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma_rsi = ma.SMA(self.__rsi, 15)
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 2)
        self.__position = None
        self.__instrument = instrument
        self.info("__instrument: {}".format(self.__instrument))


        self.__rsi_1 = rsi.RSI(feed[instrument_1].getCloseDataSeries(), 14)
        self.__sma_rsi_1 = ma.SMA(self.__rsi_1, 15)
        self.__sma_1 = ma.SMA(feed[instrument_1].getCloseDataSeries(), 2)
        self.__instrument_1 = instrument_1

    def onBars(self, bars):  # 每一个数据都会抵达这里，
        # SMA的计算存在窗口，所以前面的几个bar下是没有SMA的数据的.
        if self.__sma[-1] is None:
            return
        elif self.__sma_1[-1] is None:
            return
        # bar.getTyoicalPrice = (bar.getHigh() + bar.getLow() + bar.getClose())/ 3.0

        bar = bars[self.__instrument]
        bar_1 = bars[self.__instrument_1]
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:  # 如果手上没有头寸，那么
            if bar.getPrice() > self.__sma[-1]:
                # 开多，如果现价大于移动均线，且当前没有头寸.
                self.__position = self.enterLong(self.__instrument, 100, True)
        # 当前有多头头寸，平掉多头头寸.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()

        if self.__position is None:  # 如果手上没有头寸，那么
            if bar_1.getPrice() > self.__sma_1[-1]:
                # 开多，如果现价大于移动均线，且当前没有头寸.
                self.__position = self.enterLong(self.__instrument_1, 100, True)
        # 当前有多头头寸，平掉多头头寸.
        elif bar_1.getPrice() < self.__sma_1[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


if __name__ == '__main__':
    # 获得回测数据
    feed = Feed(Frequency.SECOND)

    feed.loadBars('bitmex_LTCZ18', test_back=True)
    feed.loadBars('okex_LIGHTBTC', test_back=True)
    myStrategy = MyStrategy(feed, *(feed.getKeys()))
    myStrategy.run()

    myStrategy.info("Final portfolio value: $%.10f" % myStrategy.getResult())
