#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/5 0:01 By xycfree
# @Descript:
import time

import websocket

sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart/rP0mQCuj/&date=2018_12_04-12_00"

def socket_conn():
    while 1:
        ws = websocket.WebSocket()
        # 建立websocket连接，这里传入了 header ，需要注意header的写入方式
        ws.connect(sock_adress,
                   header=["Accept-Encoding:gzip, deflate, br",
                           "Accept-Language:zh-CN,zh;q=0.9",
                           "Cache-Control:no-cache",
                           "Connection:Upgrade",
                           "Cookie:__utmc=226258911; __utmz=226258911.1543933608.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sessionid=8ekew6x1bmmuv6l5ohcsuvzhpw3rgivi; png=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; etg=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; cachec=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; tv_ecuid=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; km_ni=bingpoli%40gmail.com; km_lv=x; km_ai=bingpoli%40gmail.com; _sp_id.cf1a=97499503-6490-448e-a43c-e11e5ceef0ec.1543933609.3.1543943876.1543936635.62b716d5-014f-492d-acb7-619e9ebd2c7e; kvcd=1543943877185; __utma=226258911.1603730878.1543933608.1543943876.1543943876.4; __utmb=226258911.2.8.1544023100015",
                           "Host:data.tradingview.com",
                           "Origin:https://cn.tradingview.com",
                           "Pragma:no-cache",
                           "Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits",
                           "Sec-WebSocket-Key:ybGlRKHpl2FMelXXyJYs/Q==",
                           "Sec-WebSocket-Version:13",
                           "Upgrade:websocket",
                           "User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                           ])
        if ws.connected:
            # 接收实时数据，并打印出来
            try:
                with open("aa.txt", mode='a+', encoding='utf-8') as f:
                    f.write(ws.recv())
                    f.write('\n============================\n')
                    print('wait time....')
                    # print(ws.recv())
                    # 关闭连接
                    # ws.close()
            except Exception as e:
                print(e)

