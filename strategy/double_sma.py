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
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma_rsi = ma.SMA(self.__rsi, 15)
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 2)
        self.__instrument = instrument

    def onBars(self, bars):  # 每一个数据都会抵达这里
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__sma[-1], self.__sma_rsi[-1]))  # 我们打印输出收盘价与两分钟均线值

if __name__ == '__main__':
    # 获得回测数据
    feed = Feed(Frequency.MINUTE)
    # feed1 = Feed(Frequency.MINUTE)
    # feed.addBarsFromSequence('bitmex_BCHZ18', feed.loadBars('bitmex_BCHZ18'))
    feed.addBarsFromSequence(feed.loadBars("okex_LIGHTUSDT"))
    # feed.loadBars('bitmex_BCHZ18')
    feed.loadBars('okex_LIGHTUSDT')

    # 把策略跑起来
    myStrategy = MyStrategy(feed, 'okex_LIGHTUSDT')
    # myStrategy1 = MyStrategy(feed, 'okex_LIGHTUSDT')
    # myStrategy.run()
    # myStrategy1.run()

    # 3.加入分析器
    retAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(retAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    myStrategy.attachAnalyzer(sharpeRatioAnalyzer)

    # 4.运行策略
    myStrategy.run()
    # myStrategy.run()
    # myStrategy1.run()


    # 5.输出结果
    print("Final portfolio value: $%.2f" % myStrategy.getResult())

    print("Anual return: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))

    print("Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100))

    print("Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns())))
    print("Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0)))
