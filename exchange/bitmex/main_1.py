from datetime import datetime
from pyalgotrade import strategy
from pyalgotrade import broker
from pyalgotrade.bar import Frequency
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns
# from exchange.bitmex.liveApi.livebarfeed import LiveFeed
from exchange.bitmex.liveApi.livebarfeed import LiveFeed
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

from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
from ccwt_client.ccwt_feed import Feed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi



# 构建一个策略
class MyStrategy(strategy.BaseStrategy):
    def __init__(self, feed, instrument, brk):
        super(MyStrategy, self).__init__(feed, brk)
        logger.info("========MyStrategy init=======")
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma_rsi = ma.SMA(self.__rsi, 15)
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 2)
        logger.info("__sma: {}".format(self.__sma))

        self.__instrument = instrument


    def onBars(self, bars):  # 每一个数据都会抵达这里
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__sma[-1], self.__sma_rsi[-1]))  # 我们打印输出收盘价与两分钟均线值


def run_strategy():
    logger.info("-------START-------")
    feed = LiveFeed([COIN_TYPE], Frequency.MINUTE, REQ_DELAY)
    liveBroker = LiveBroker(COIN_TYPE, BitmexClient(COIN_TYPE))
    myStrategy = MyStrategy(feed, COIN_TYPE, liveBroker)
    myStrategy.run()





    # feed = LiveFeed([COIN_TYPE], Frequency.MINUTE, REQ_DELAY)
    # liveBroker = LiveBroker(COIN_TYPE, BitmexClient(COIN_TYPE))
    # from exchange.bitmex.api_keys import API_KEY, API_SECRET
    # _symbol = "btcusdt"
    # _bitmex = BitmexClient(_symbol)
    #
    # frequency = bar.Frequency.MINUTE
    # _bitmex.apiKey = API_KEY
    # _bitmex.secret = API_SECRET
    # res = _bitmex.get_ticker(_symbol, params={"binSize": '5m', 'count': '100'})
    # print('res is len: {}'.format(res[0]))
    # feed = []
    # for row in res:
    #     try:
    #         feed.append(bar.BasicBar(datetime.strptime(datetime.strftime(
    #             datetime.strptime(row.get('datetime'), "%Y-%m-%dT%H:%M:%S%sZ"), "%Y-%m-%d %H:%M:%S"),
    #             "%Y-%m-%d %H:%M:%S"), row.get('open', 0) or row.get('preclose', 0), row.get('high', 0),
    #             row.get('low', 0),
    #             row.get('close', 0), row.get('volume', 0) or row.get('quoteVolume', 0), frequency)
    #             )
    #     except:
    #         pass
    #
    # myStrategy = MyStrategy(feed, COIN_TYPE, liveBroker)
    # myStrategy.run()


if __name__ == '__main__':
    run_strategy()
