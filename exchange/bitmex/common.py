#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/11/23 13:57    @Author  : xycfree
# @Descript: 
from coinmarketcap import Market

def base_usdt_price(coin=''):
    res = Market().ticker(coin)
    return res

if __name__ == '__main__':
    res = base_usdt_price()
    print(res)