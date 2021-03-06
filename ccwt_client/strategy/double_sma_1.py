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
    _instrument = ''
    def __init__(self, feed):
        super(MyStrategy, self).__init__(feed)
        self.__position = None
        # self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        # self.__instrument = instrument
        self.getBroker()

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at %.10f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.10f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()


    def onBars(self, bars):  # 每一个数据都会抵达这里，
        self.info('double sma 1 onBars bar: {}'.format(bars.getInstruments()))
        # SMA的计算存在窗口，所以前面的几个bar下是没有SMA的数据的.
        if self.__sma[-1] is None:
            return
        bar = bars[self.__instrument]

        # # If a position was not opened, check if we should enter a long position.
        if self.__position is None:  # 如果手上没有头寸，那么
            if bar.getPrice() > self.__sma[-1]:
                # 开多，如果现价大于移动均线，且当前没有头寸.
                self.__position = self.enterLong(self.__instrument, 100, True)
        # 当前有多头头寸，平掉多头头寸.
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()


if __name__ == '__main__':
    # 获得回测数据
    feed = Feed(Frequency.SECOND)

    feed.loadBars('bitmex_LTCZ18', test_back=True)
    feed.loadBars('okex_LIGHTBTC', test_back=True)
    myStrategy = MyStrategy(feed)  # , ('bitmex_LTCZ18', "okex_LIGHTBTC")
    retAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(retAnalyzer)
    sharpRatioAnalyzer = sharpe.SharpeRatio()
    myStrategy.attachAnalyzer(sharpRatioAnalyzer)

    myStrategy.run()

    myStrategy.info("Final portfolio value: $%.10f" % myStrategy.getResult())
    print("Final portfolio value: $%.2f" % myStrategy.getResult())
    print("Anual return: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
    print("Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100))
    print("Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns())))
    print("Sharpe ratio: %.2f" % (sharpRatioAnalyzer.getSharpeRatio(0)) )
