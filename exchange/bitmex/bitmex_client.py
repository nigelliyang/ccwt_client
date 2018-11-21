from exchange.bitmex.liveApi.TradeClientBase import *
from exchange.bitmex.liveApi.liveUtils import *
from pyalgotrade.utils import dt
from exchange.bitmex.liveApi import liveLogger

from exchange.bitmex.bitmex_sdk import ApiClient, ApiError
from exchange.bitmex.bitmex import Bitmex
from exchange.bitmex.api_keys import API_KEY
from exchange.bitmex.api_keys import API_SECRET

# https://github.com/huobiapi/API_Docs/wiki
# https://github.com/huobiapi/API_Docs/wiki/REST_api_reference
logger = liveLogger.getLiveLogger("bitmex_client")
bitmex = Bitmex()
bitmex.apiKey = API_KEY
bitmex.secret = API_SECRET


def Str2float(func):
    def waper(*args, **kwargs):
        return float(func(*args, **kwargs))

    return waper


class BitmexOrderType(object):
    BuyLimit = 'buy-limit'  # 限价买
    BuyMarket = 'buy-market'  # 市价买
    SellLimit = 'sell-limit'  # 限价卖
    SellMarket = 'sell-market'  # 市价卖


class BitmexOrderState(object):
    OrderFilled = 'filled'  # 完全成交
    OrderCanceled = 'canceled'  # 取消
    OrderSubmited = 'submitted'  # 提交
    """
    submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, 
                filled 完全成交, canceled 已撤销
    """


class BitmexTradeOrder(TradeOrderBase):
    def __init__(self, obj):
        self.__obj = obj
        super(BitmexTradeOrder, self).__init__()

    def getId(self):
        return self.__obj.id

    def isBuy(self):
        return self.__obj.type in (BitmexOrderType.BuyLimit, BitmexOrderType.BuyMarket)

    def isSell(self):
        return not self.isBuy()

    @Str2float
    def getPrice(self):
        return self.__obj.price

    @Str2float
    def getAmount(self):
        return self.__obj.amount

    def getDateTime(self):
        return dt.timestamp_to_datetime(int(self.__obj['created-at']) / 1000)


# GET /v1/order/orders/{order-id}/matchresults
class BitmexTradeUserTransaction(TradeUserTransactionBase):
    def __init__(self, obj):
        self.__obj = obj

    @Str2float
    def getBTC(self):
        return self.__obj['field-amount']

    @Str2float
    def getBTCUSD(self):
        # return self.__obj['field-cash-amount']
        return self.__obj['price']

    @Str2float
    def getFee(self):
        return self.__obj['field-fees']

    def getOrderId(self):
        return self.__obj['id']

    def isFilled(self):
        return self.__obj['state'] == BitmexOrderState.OrderFilled

    def getDateTime(self):
        return dt.timestamp_to_datetime(int(self.__obj['finished-at']) / 1000)


class BitmexTradeAccountBalance(TradeAccountBalanceBase):
    def __init__(self, obj):
        self.__obj = obj

    def getUSDAvailable(self):
        return self.__obj['usdt']

    def getBTCAvailable(self):
        return self.__obj['coin']


class BitmexCoinType():
    def __init__(self, coin, cash):
        self.__coin = coin
        self.__cash = cash
        self.__symbol = coin + cash

    def getCoin(self):
        return self.__coin

    def getCash(self):
        return self.__cash

    def getSymbol(self):
        return self.__symbol

    def __str__(self):
        return self.getSymbol()


class BitmexAccountBalance():
    def __init__(self, instrument, obj):
        self.__coin = 0
        self.__cash = 0
        balances = obj.get('list')
        if balances is None:
            return
        for x in balances:
            if x.currency == instrument.getCoin() and x.type == 'trade':
                self.__coin = x.balance
            elif x.currency == instrument.getCash() and x.type == 'trade':
                self.__cash = x.balance

    @Str2float
    def getCash(self):
        return self.__cash

    @Str2float
    def getCoin(self):
        return self.__coin


class BitmexTradeClient(TradeClientBase):
    def __init__(self, instrument):
        self.__coinType = instrument
        self.__client = ApiClient(API_KEY, API_SECRET)
        self.__accountid = self.getAccountId()

    @tryForever
    def getAccountId(self):
        """查询当前用户的所有账户"""
        accs = self.__client.get('/v1/account/accounts')
        for x in accs:
            if x.type == 'spot' and x.state == 'working':
                return x.id
        raise Exception('no active account ID!')

    # --
    # @exceDebug
    def getAccountBalance(self):
        """获取账户余额"""
        # balances = self.__client.get('/v1/account/accounts/%s/balance' % self.__accountid)
        balances = bit.fetch_balance()
        logger.info("balance: {}".format(balances))
        acc = BitmexAccountBalance(self.__coinType, balances)

        logger.info('getAccountBalance: usdt:%s coin:%s' % (acc.getCash(), acc.getCoin()))
        return BitmexTradeAccountBalance({'usdt': acc.getCash(), 'coin': acc.getCoin()})

    # --
    # @exceDebug
    def getOpenOrders(self):
        logger.info('getOpenOrders:')
        return []
        """
        return [hbTradeOrder({
            'id': ID(),
            'isBuy' : True,
            'price' : 13990.99,
            'amount' : 1.1234,
            'time' : datetime.datetime.utcnow(),
        })]
        """

    # --
    # @exceDebug
    def cancelOrder(self, orderId):
        """取消订单"""
        logger.info('cancelOrder:%s' % orderId)
        self.__client.post('/v1/order/orders/%s/submitcancel' % orderId)
        self.checkOrderState(orderId, [BitmexOrderState.OrderCanceled, BitmexOrderState.OrderFilled])

    # --
    # @exceDebug
    def buyLimit(self, limitPrice, quantity):
        """限价买"""
        logger.info('buyLimit:%s %s' % (limitPrice, quantity))
        orderInfo = self.postOrder(limitPrice, quantity, BitmexOrderType.BuyLimit)
        return BitmexTradeOrder(orderInfo)

    # --
    # @exceDebug
    def sellLimit(self, limitPrice, quantity):
        """限价卖"""
        logger.info('sellLimit:%s %s' % (limitPrice, quantity))
        orderInfo = self.postOrder(limitPrice, quantity, BitmexOrderType.SellLimit)
        return BitmexTradeOrder(orderInfo)

    # --
    # @exceDebug
    def getUserTransactions(self, ordersId):
        """查询当前委托、历史委托"""
        if len(ordersId):
            logger.info('getUserTransactions:%s' % ordersId)
        ret = []
        for oid in ordersId:
            orderInfo = self.__client.get('/v1/order/orders/%s' % oid)
            ret.append(BitmexTradeUserTransaction(orderInfo))
        return ret

    def postOrder(self, limitPrice, quantity, orderType):
        """创建并执行订单"""
        price = str(PriceRound(limitPrice))
        amount = str(CoinRound(quantity))
        order_id = self.__client.post('/v1/order/orders', {
            'account-id': self.__accountid,
            'amount': amount,
            'price': price,
            'symbol': self.__coinType.getSymbol(),
            'type': orderType,
            'source': 'api'
        })
        self.activeOrder(order_id)
        orderInfo = self.checkOrderState(order_id, [BitmexOrderState.OrderSubmited, BitmexOrderState.OrderFilled])
        return orderInfo

    @tryForever
    def checkOrderState(self, orderid, states):
        """查询一个订单详情
            states:
                submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销,
                filled 完全成交, canceled 已撤销
        """
        orderInfo = self.__client.get('/v1/order/orders/%s' % orderid)
        if orderInfo.state in states:
            return orderInfo
        raise Exception('wait state:%s => %s' % (orderInfo.state, states))

        orderInfo = bitmex.fetch_order(orderid, )




    @tryForever
    def activeOrder(self, orderid):
        """活动的订单"""
        return self.__client.post('/v1/order/orders/%s/place' % orderid)
