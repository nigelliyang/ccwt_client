#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/11/13 17:23    @Author  : xycfree
# @Descript:  sma 简单交叉线策略

from pyalgotrade import strategy, plotter
from pyalgotrade.bar import Frequency
from pyalgotrade.stratanalyzer import returns, sharpe
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade.utils import stats

from ccwt_client import Feed


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        # self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                # shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())  # 现金
                shares = int(self.getBroker().getEquity() * 0.9 / bars[self.__instrument].getPrice())  # 现价+ 投资组合
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)  # 生成一个多头买进订单
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()


if __name__ == '__main__':
    feed = Feed(Frequency.SECOND)

    feed.loadBars('bitmex_LTCZ18', test_back=True)
    # feed.loadBars('okex_LIGHTBTC', test_back=True)
    myStrategy = SMACrossOver(feed, 'bitmex_LTCZ18', 10)

    # =========================START=================================== #
    sharpe_ratio = sharpe.SharpeRatio()
    myStrategy.attachAnalyzer(sharpe_ratio)
    plt = plotter.StrategyPlotter(myStrategy)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot("binance_TRXBTC").addDataSeries("SMA", myStrategy.getSMA())
    # Plot the simple returns on each bar.
    # plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    # 5.运行策略
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.10f" % myStrategy.getResult())
    # 6.输出夏普率、绘图
    print("sharpe_ratio")
    print(sharpe_ratio.getSharpeRatio(0))
    plt.plot()
    # ========================END============================== #

    # =======================START=============================== #
    # retAnalyzer = returns.Returns()
    # myStrategy.attachAnalyzer(retAnalyzer)
    # sharpRatioAnalyzer = sharpe.SharpeRatio()
    # myStrategy.attachAnalyzer(sharpRatioAnalyzer)
    # myStrategy.run()
    # myStrategy.info("Final portfolio value: $%.10f" % myStrategy.getResult())
    # print("Final portfolio value: $%.2f" % myStrategy.getResult())
    # print("Anual return: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
    # print("Average daily return: %.2f %%" % (stats.mean(retAnalyzer.getReturns()) * 100))
    # print("Std. dev. daily return: %.4f" % (stats.stddev(retAnalyzer.getReturns())))
    # print("Sharpe ratio: %.2f" % (sharpRatioAnalyzer.getSharpeRatio(0)))
    # ========================================================= #
