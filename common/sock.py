#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/5 0:01 By xycfree
# @Descript:
import time

import websocket

sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart%2FrP0mQCuj%2F&date=2018_12_06-18_19"

def socket_conn():
    ws = websocket.WebSocket()
    # 建立websocket连接，这里传入了 header ，需要注意header的写入方式
    ws.connect(sock_adress,
               header=["Accept-Encoding:gzip, deflate, br",
                       "Accept-Language:zh-CN,zh;q=0.9",
                       "Cache-Control:no-cache",
                       "Connection:Upgrade",
                       "Cookie:__utmc=226258911; sessionid=8ekew6x1bmmuv6l5ohcsuvzhpw3rgivi; png=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; etg=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; cachec=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; tv_ecuid=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; km_ni=bingpoli%40gmail.com; km_lv=x; km_ai=bingpoli%40gmail.com; __utmz=226258911.1544029652.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.1603730878.1543933608; _gid=GA1.2.756612978.1544029766; __utma=226258911.1603730878.1543933608.1544029886.1544113223.8; _sp_ses.cf1a=*; km_vs=1; __utmt=1; _sp_id.cf1a=97499503-6490-448e-a43c-e11e5ceef0ec.1543933609.6.1544113911.1544029886.fb53bca2-9d82-4488-84bb-bd5042275f72; kvcd=1544113912049; __utmb=226258911.39.9.1544114040942",
                       "Host:data.tradingview.com",
                       "Origin:https://cn.tradingview.com",
                       "Pragma:no-cache",
                       "Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits",
                       "Sec-WebSocket-Key:kjw7Ux+3nwGs4xgsBEYSmg==",
                       "Sec-WebSocket-Version:13",
                       "Upgrade:websocket",
                       "User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                       ])
    print('start...')
    print(ws.recv())
    # print(ws.recv_data())
    req = '~m~42~m~{"m":"protocol_switched","p":["protobuf"]}'
    print(req)
    ws.send(req)
    print(ws.recv())
    # while 1:
    #     if ws.connected:
    #         req = '~m~59~m~{"m":"request_more_data","p":["cs_NUaSsV3pUYb9","s1",1183]}'
    #         print(req)
    #         ws.send(req)
    #         # 接收实时数据，并打印出来
    #         try:
    #             print(ws.recv())
    #             # 关闭连接
    #             # ws.close()
    #             # time.sleep(1)
    #
    #         except Exception as e:
    #             print(e)

socket_conn()