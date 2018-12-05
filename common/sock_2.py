#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/6 0:17 By xycfree
# @Descript:

import websocket

def on_message(ws, message):
    # 服务器有数据更新时，主动推送过来的数据
    print(message)

def on_error(ws, error):
    # 程序报错时，就会触发on_error事件
    print(error)

def on_close(ws):
    print("Connection closed ……")

def on_open(ws):
    # 连接到服务器之后就会触发on_open事件，这里用于send数据
    req = '{"event":"subscribe", "channel":"btc_usdt.deep"}'
    print(req)
    # ws.send(req)

if __name__ == "__main__":
    sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart/rP0mQCuj/&date=2018_12_04-12_00"
    headers = [
        ("Accept-Encoding", "gzip, deflate, br"),
        ("Accept-Language", "zh-CN,zh;q=0.9"),
        ("Cache-Control", "no-cache"),
        ("Connection", "Upgrade"),
        ("Cookie",
         "__utmc=226258911; __utmz=226258911.1543933608.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sessionid=8ekew6x1bmmuv6l5ohcsuvzhpw3rgivi; png=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; etg=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; cachec=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; tv_ecuid=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; km_ni=bingpoli%40gmail.com; km_lv=x; km_ai=bingpoli%40gmail.com; __utma=226258911.1603730878.1543933608.1543943876.1543943876.4; _sp_id.cf1a=97499503-6490-448e-a43c-e11e5ceef0ec.1543933609.4.1544024554.1543943876.044c0ae5-a149-4f0a-b8b8-4dec02dab71a; kvcd=1544024555205"),
        ("Host", "data.tradingview.com"),
        ("Origin", "https://cn.tradingview.com"),
        ("Pragma", "no-cache"),
        ("Sec-WebSocket-Extensions", "permessage-deflate; client_max_window_bits"),
        ("Sec-WebSocket-Key", "9rOfdwbM9cEry9bVrs1cOg=="),
        ("Sec-WebSocket-Version", "13"),
        ("Upgrade", "websocket"),
        ("User-Agent",
         "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"),
    ]
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(sock_adress, header=headers,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_timeout=30)
