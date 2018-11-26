#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/11/23 13:57    @Author  : xycfree
# @Descript: 
from coinmarketcap import Market
from pyalgotrade import logger as log

logger = log.getLogger("common")
def base_usdt_price(coin=''):
    """   Valid cryptocurrency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"
        id:  1 BTC    2 LTC    1321 ETH    52:XRP  1831  BCH
    """
    if not coin:
        _id = '1'
    elif coin.upper() == 'BTC':
        _id = "1"
    elif coin.upper() == "LTC":
        _id = "2"
    elif coin.upper() == 'ETH':
        _id = "1321"
    elif coin.upper() == 'XRP':
        _id = "52"
    elif coin.upper() == 'BCH':
        _id = '1831'
    else:
        _id = ""
    if _id:
        data = Market().ticker(currency=_id).get('data', {})
        logger.info("data: {}".format(data))
        if not data:
            return 0
        usd_price = data.get('quotes', {}).get('USD', {}).get('price')
        return round(usd_price, 4)
    else:
        raise KeyError('Valid cryptocurrency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"')

if __name__ == '__main__':
    res = base_usdt_price('btc')
    print(res)