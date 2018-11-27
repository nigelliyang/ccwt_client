from datetime import datetime
from pyalgotrade import strategy
from pyalgotrade import broker
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns
# from exchange.bitmex.liveApi.livebarfeed import LiveFeed
from exchange.bitmex.liveApi.livebroker import LiveBroker
from exchange.bitmex.bitmex import Bitmex
from exchange.bitmex.bitmex_client import BitmexTradeClient as BitmexClient
from exchange.bitmex.bitmex_client import BitmexCoinType
# from exchange.bitmex.liveApi import liveLogger
from pyalgotrade import bar

from pyalgotrade import logger as log

# logger = liveLogger.getLiveLogger("MyStrategy")

logger = log.getLogger("MyStrategy")

COIN_TYPE = BitmexCoinType('btc', 'usdt')
K_PERIOD = 60
REQ_DELAY = 0

class MyStrategy(strategy.BaseStrategy):
    def __init__(self, feed, instrument, brk):
        super(MyStrategy, self).__init__(feed, brk)
        self.__position = None
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = {}
        self.__sma[60] = ma.SMA(self.__prices, 60)
        self.__sma[10] = ma.SMA(self.__prices, 10)
        self.__sma[30] = ma.SMA(self.__prices, 30)

    def getSMA(self, period):
        return self.__sma[period]

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        logger.info("BUY at $%.2f %.4f" % (execInfo.getPrice(), execInfo.getQuantity()))

    def onEnterCanceled(self, position):
        logger.info("onEnterCanceled")
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        logger.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        logger.info("onExitCanceled")
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        bar = bars[self.__instrument]
        if self.getFeed().isHistory():
            return
        if self.__sma[60][-1] is None:
            return
        logger.info("onBars %s:%s: close:%.2f" % (self.__instrument, bar.getDateTimeLocal(), bar.getPrice()))

        bar = bars[self.__instrument]

        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__sma[10], self.__sma[30]) > 0:
                mbroker = self.getBroker()
                shares = mbroker.getCash() / bar.getPrice() * 0.9
                self.__position = self.enterLongLimit(self.__instrument, bar.getPrice(), shares, True)
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__sma[10], self.__sma[30]) > 0:
            self.__position.exitLimit(bar.getPrice())


def run_strategy():
    logger.info("-------START-------")
    # feed = LiveFeed([COIN_TYPE], Frequency.MINUTE, REQ_DELAY)
    liveBroker = LiveBroker(COIN_TYPE, BitmexClient(COIN_TYPE))
    from exchange.bitmex.api_keys import API_KEY, API_SECRET
    _bitmex = Bitmex()
    _symbol = "XBTZ18"
    frequency = bar.Frequency.MINUTE
    _bitmex.apiKey = API_KEY
    _bitmex.secret = API_SECRET
    res = _bitmex.fetch_ticker(_symbol, params={"binSize": '5m', 'count': '100'})
    print('res is len: {}'.format(res[0]))
    feed = []
    for row in res:
        try:
            feed.append(bar.BasicBar(datetime.strptime(datetime.strftime(
                datetime.strptime(row.get('datetime'), "%Y-%m-%dT%H:%M:%S%sZ"), "%Y-%m-%d %H:%M:%S"),
                "%Y-%m-%d %H:%M:%S"), row.get('open', 0) or row.get('preclose', 0), row.get('high', 0),
                row.get('low', 0),
                row.get('close', 0), row.get('volume', 0) or row.get('quoteVolume', 0), frequency)
                )
        except:
            pass

    myStrategy = MyStrategy(feed, _symbol, liveBroker)
    myStrategy.run()


if __name__ == '__main__':
    run_strategy()
