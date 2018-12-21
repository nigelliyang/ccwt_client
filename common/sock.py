#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/5 0:01 By xycfree
# @Descript:
import time

import websocket

sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart%2FrP0mQCuj%2F&date=2018_12_13-11_47"

def socket_conn():
    ws = websocket.WebSocket()
    # 建立websocket连接，这里传入了 header ，需要注意header的写入方式
    ws.connect(sock_adress,
               header=["Accept-Encoding:gzip, deflate, br",
                       "Accept-Language:zh-CN,zh;q=0.9",
                       "Cache-Control:no-cache",
                       "Connection:Upgrade",
                       "Cookie:sessionid=8ekew6x1bmmuv6l5ohcsuvzhpw3rgivi; tv_ecuid=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; km_ni=bingpoli%40gmail.com; km_lv=x; km_ai=bingpoli%40gmail.com; __utmz=226258911.1544029652.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.1603730878.1543933608; __utma=226258911.1603730878.1543933608.1544196238.1544196238.24; __utmc=226258911; __utmt=1; _sp_ses.cf1a=*; km_vs=1; _sp_id.cf1a=97499503-6490-448e-a43c-e11e5ceef0ec.1543933609.8.1544713475.1544196238.eb1bd66e-ef1b-4689-a64c-6293ecaa168f; kvcd=1544713474809; __utmb=226258911.15.9.1544713538190",
                       "Host:data.tradingview.com",
                       "Origin:https://cn.tradingview.com",
                       "Pragma:no-cache",
                       "Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits",
                       "Sec-WebSocket-Key:CsSSefIwhq6mYFASYsZb3A==",
                       "Sec-WebSocket-Version:13",
                       "Upgrade:websocket",
                       "User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                       ])
    while 1:

        if ws.connected:
            # 接收实时数据，并打印出来
            ws.send('~m~55~m~{"m":"chart_create_session","p":["cs_kllUhspHvjaI",""]}')
            ws.send('~m~75~m~{"m":"create_series","p":["cs_kllUhspHvjaI","s1","s1","symbol_1","45",300]}')
            ws.send('~m~57~m~{"m":"request_more_data","p":["cs_kllUhspHvjaI","s1",27]}')
            try:
                print(ws.recv())
                # print(ws.next())
                # print(ws.recv_data_frame())  # [1, <websocket._abnf.ABNF object at 0x0000000009D9A438>]

                # print(ws.recv_data())
                # print(ws.recv_frame())
                # 关闭连接
                # ws.close()
                # time.sleep(1)

            except Exception as e:
                print(e)

socket_conn()