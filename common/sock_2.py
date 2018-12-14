#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/6 0:17 By xycfree
# @Descript:
import json
import struct

import websocket


def write_msg(message):
    data = struct.pack('B', 129)  # 写入第一个字节 10000001
    # 写入包长度
    msg_len = len(message)
    if msg_len <= 125:
        data += struct.pack('B', msg_len)
    elif msg_len <= (2 ** 16 - 1):
        data += struct.pack('!BH', 126, msg_len)
    elif msg_len <= (2 ** 64 - 1):
        data += struct.pack('!BQ', 127, msg_len)
    else:
        print('to long message')
        return
    data += bytes(message, encoding='utf-8')
    print(data)
    return data


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
    req = '~m~507~m~{"m":"create_study","p":["cs_EiEhUrVVF8xU","st5","st1","s1","ESD@tv-scripting-101!",{"text":"jVYYHlybeYXP+v3jp6OkRg==_8m/G1bDZkrazHNATuRuAm6b93qQ45WVQoUlOAUtDVflVOSylmoQjRwLtqw2WsuAdL/UomLVEdeWFDQIvydXrC95PxxspNhwDf39U7YO0Wf0GW2C5L7IiGR+bbDuCbRd1ERrZ1zfLksH3nAWXQm90ASnmCyvOLtLAj9z3KAdkSkD5pPlAEl1iM1e8iw3TDSxz4Btdx7TnwInlDZCce1tS0M9kSy4R+1IpF1WBX/22VjCeEENP2nObjvKlFpUEMFb4GiL/UkynOUnwCLtPDyfh1A+5Y8K/5pM/Qkvd106X3Snke/gmOeCxyNjBCNmiv2ve9XtViDz4hKWVDLgAwjyipVM=","pineId":"TV_SPLITS","pineVersion":"2.0"}]}'
    # req = write_msg(req)
    # print(req)
    # ws.send(json.dumps(req, ensure_ascii=False))
    ws.send(req)
    print('on_open')


if __name__ == "__main__":
    sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart%2FrP0mQCuj%2F&date=2018_12_13-11_47"
    headers = ["Accept-Encoding:gzip, deflate, br",
               "Accept-Language:zh-CN,zh;q=0.9",
               "Cache-Control:no-cache",
               "Connection:Upgrade",
               "Cookie:sessionid=8ekew6x1bmmuv6l5ohcsuvzhpw3rgivi; tv_ecuid=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; km_ni=bingpoli%40gmail.com; km_lv=x; km_ai=bingpoli%40gmail.com; __utmz=226258911.1544029652.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.1603730878.1543933608; __utmc=226258911; _sp_id.cf1a=97499503-6490-448e-a43c-e11e5ceef0ec.1543933609.8.1544714838.1544196238.eb1bd66e-ef1b-4689-a64c-6293ecaa168f; kvcd=1544714839407; __utma=226258911.1603730878.1543933608.1544714838.1544714838.28; __utmb=226258911.4.9.1544805295968",
               "Host:data.tradingview.com",
               "Origin:https://cn.tradingview.com",
               "Pragma:no-cache",
               "Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits",
               "Sec-WebSocket-Key:u7yhZIX6CKA8pRmx6e4tCg==",
               "Sec-WebSocket-Version:13",
               "Upgrade:websocket",
               "User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
               ]
    # websocket.enableTrace(True)
    websocket.enableTrace(False)

    ws = websocket.WebSocketApp(sock_adress, header=headers,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_timeout=30)
