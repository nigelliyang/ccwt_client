#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.broker.backtesting import Broker
from pyalgotrade.broker.backtesting import TradePercentage
from pyalgotrade.broker.slippage import VolumeShareSlippage
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from ccwt_client.ccwt_feed import Feed

class MultiSymbols(strategy.BacktestingStrategy):
    def __init__(self, feed, instruments, broker):
        strategy.BacktestingStrategy.__init__(self, feed, broker)
        self.__instruments = instruments
        self.__sharesToBuy = {}

        # Initialize indicators for each instrument.
        ''' 技术指标
            SMA、EMA、WMA、VMAP、MACD、RSI、StochasticOscillator、BollingerBands、ATR、HurstExponent
            CumulativeReturn、LeastSquaresRegression、Slope、StdDev、ZScore
        '''
        self.__sma = {}
        for instrument in instruments:
            priceDS = feed[instrument].getPriceDataSeries()
            self.__sma[instrument] = ma.SMA(priceDS, 15)

    def getSMA(self, instrument):
        return self.__sma[instrument]


    def onBars(self, bars):
        #获取多标的的bar
        #for instrument in bars.getInstruments():
        #    self.info('%s price: %.6f' % (instrument, bars.getBar(instrument).getClose()))
        orders = self.getBroker().getActiveOrders('okex_BTCUSDT')
        if orders:
            self.info(str(orders))
        bitmex = bars.getBar('bitmex_XBTUSD')
        okex = bars.getBar('okex_BTCUSDT')
        bitmexSMA = self.getSMA('bitmex_XBTUSD')
        if bitmex is None:
            return None
        if okex is None:
            return None
        if bitmexSMA[-1] is None:
            return None
        if bitmex is not None and okex is not None:
            if bitmex.getClose() - okex.getClose() > 3 and bitmex.getClose() > bitmexSMA[-1]:
                cash = self.getBroker().getCash()
                size = cash * 0.1 / okex.getClose()
                '''
                size > 0  buy ;  size < 0  sell;
                marketOrder:以市场价成交 onClose : True,用下一个bar的收盘价; False: 用下一个bar的开盘价,目前onClose True不支持一天内的bar
                limitOrder:限价成交 
                    buy:如果下一个bar低于limitPrice，成交价=开盘价;如果下一个bar包含limitPrice，成交价=min(open,limitPrice)
                    sell:如果下一个bar高于limitPrice，成交价=开盘价;如果下一个bar包含limitPrice，成交价=max(open,limitPrice)
                stopOrder:止损单
                    buy:如果下一个bar高于stopPrice,成交价=开盘价;如果包含stopPrice，成交价=max(open,stopPrice)
                    sell:如果下一个bar低于stopPrice,成交价=开盘价;如果包含stopPrice，成交价=min(open,stopPrice)
                stopLimitOrder:限价止损单
                    先判断是否到达止损价，然后再判断是否到了限定价格   
                '''
                self.marketOrder('okex_BTCUSDT', size)
                self.info('cash %.2f ; size %.2f' % (cash, size))
                self.info('bitmex price %.6f ; okex price %.6f ; bitmexSMA %.6f' % (bitmex.getClose(), okex.getClose(), bitmexSMA[-1]))

            if bitmex.getClose() - okex.getClose() < 4 and bitmex.getClose() < bitmexSMA[-1]:
                okexShares = self.getBroker().getShares('okex_BTCUSDT')
                size = okexShares * -0.5
                self.marketOrder('okex_BTCUSDT', size)
                self.info('okexShares %.2f ; size %.2f' % (okexShares, size))
                self.info('bitmex price %.6f ; okex price %.6f ; bitmexSMA %.6f' % (bitmex.getClose(), okex.getClose(), bitmexSMA[-1]))

def main(plot):

    instruments = ['bitmex_XBTUSD','okex_BTCUSDT']
    feed = Feed(Frequency.SECOND)
    feed.loadBars("bitmex_XBTUSD", test_back=True)
    feed.loadBars("okex_BTCUSDT", test_back=True)

    '''初始保证金'''
    initCash = 1000000
    '''手续费设置
        目前不支持多标的设置不同的手续费类型 
        3种手续费类型：
        NoCommission：None 默认
        FixedPerTrade：固定金额
        TradePercentage：按比例收费
    '''
    commission = TradePercentage(0.0003)
    broker = Broker(initCash,feed,commission)

    #设置为滑点模型，默认为 NoSlippage
    #broker.getFillStrategy().setSlippageModel(VolumeShareSlippage)

    #设置交易量限制
    #每一个bar中的 volume * limit
    #broker.getFillStrategy().setVolumeLimit(0.1)

    strat = MultiSymbols(feed, instruments, broker)

    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    returnsAnalyzer = returns.Returns()
    strat.attachAnalyzer(returnsAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, False, False, True)
        plt.getOrCreateSubplot("cash").addCallback("Cash", lambda x: strat.getBroker().getCash())
        # Plot strategy vs. SPY cumulative returns.
        # plt.getOrCreateSubplot("returns").addDataSeries("SPY", cumret.CumulativeReturn(feed["SPY"].getPriceDataSeries()))
        plt.getOrCreateSubplot("returns").addDataSeries("Strategy", returnsAnalyzer.getCumulativeReturns())

    strat.run()
    print("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))
    print("Returns: %.2f %%" % (returnsAnalyzer.getCumulativeReturns()[-1] * 100))

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)