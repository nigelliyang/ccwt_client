#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/11/6 22:44 By xycfree
# @Descript: 多标策略

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
    def __init__(self, feed):
        super(MyStrategy, self).__init__(feed)
        # self.setUseAdjustedValues(True)
        orders = {
            "okex_LIGHTBTC": 1000,
            "bitmex_LTCZ18": 5000,
        }
        for instrument, quantity in orders.items():
            self.marketOrder(instrument, quantity, onClose=False, allOrNone=False)


    def onBars(self, bars):  # 每一个数据都会抵达这里，
        # self.info(bars.getBar('okex_LIGHTBTC'))
        self.info(bars.getInstruments())



if __name__ == '__main__':
    # 获得回测数据
    feed = Feed(Frequency.SECOND)

    feed.loadBars('bitmex_LTCZ18', test_back=True)
    feed.loadBars('okex_LIGHTBTC', test_back=True)
    myStrategy = MyStrategy(feed)
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
