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
    print('on_open')

    reqs = [
        '~m~55~m~{"m":"chart_create_session","p":["cs_zzchpGKpeP6K",""]}',
        '~m~52~m~{"m":"quote_create_session","p":["qs_HQrpVXxRyvLl"]}',
        '~m~268~m~{"m":"quote_set_fields","p":["qs_HQrpVXxRyvLl","ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume"]}',
        '~m~98~m~{"m":"quote_add_symbols","p":["qs_HQrpVXxRyvLl","BITFINEX:BTCUSD",{"flags":["force_permission"]}]}',
        '~m~68~m~{"m":"quote_fast_symbols","p":["qs_HQrpVXxRyvLl","BITFINEX:BTCUSD"]}',
        '~m~69~m~{"m":"request_studies_metadata","p":["cs_zzchpGKpeP6K","metadata_1"]}',
        '~m~63~m~{"m":"switch_timezone","p":["cs_zzchpGKpeP6K","Asia/Shanghai"]}',
        '~m~119~m~{"m":"resolve_symbol","p":["cs_zzchpGKpeP6K","symbol_1","={\"symbol\":\"BITFINEX:BTCUSD\",\"adjustment\":\"splits\"}"]}',
        # '~m~119~m~{"m":"resolve_symbol","p":["cs_zzchpGKpeP6K","symbol_1","={"symbol":"BITFINEX:BTCUSD","adjustment":"splits"}"]}',
        '~m~75~m~{"m":"create_series","p":["cs_zzchpGKpeP6K","s1","s1","symbol_1","45",300]}',
        '~m~126~m~{"m":"create_study","p":["cs_zzchpGKpeP6K","st1","st1","s1","Volume@tv-basicstudies-81",{"length":20,"col_prev_close":false}]}',
        '~m~2112~m~{"m":"create_study","p":["cs_zzchpGKpeP6K","st2","st1","s1","StrategyScript@tv-scripting-101!",{"text":"2sMXFZEjEcAEL0TdZuTIQA==_Ms0NAfB4PBEpsMEJL29vRZnweB9M0oyj4eO625LXy1/T6EnFjvZPYvO5V7QS+6mdXgxFthk3XpTftMC3l23+JkK6NWfL1g13DydoA5L7gSC/Vi3LAFTxx8QJMWo/u4rLgfdiZDJC1o/JWj6J0iBXmk3XiVdZroPx0NDoGSNzORqMQziSTldq7Nt/4bJB5NBzuBrtCbWd7j66GAOnTRJB7vG4SGWbkFqOv4wRbFAoOkSoMyC1/6ZeflXdWcyZGk0YPsxpcp9JOOU4dEgnHHXI+sZCCjuIv5IK+lmtwnXPhlPRyiRpqQjUDOHMQZqlO4vlmqgOuxKDeJ57tyFGaiIIuIChwStgOg4CN24pCf0SMy8wEW4rax1Y/MvlHb9qQ9HpS18ka1nGdbrGc3UHFQ25kudgsPE9wC4KiZVXSCarniMhyV6tTXt+boAH8g8U4BPaSSCNAr+lh2WNYHl/ddZJ9JaZWod/VIlPo732Ili2DZg1neeIK3O3TMTKMROB5THzE6yQnrE5GrVxY2h291GSdjt5a04ayWwpzZizvGG/e4Pug/8UWsydpjifVmhwF7purE3EdNDrXxG56uKu8Xh3RZF5A68HFcIzpXYSyefNxcfN0MsTfHnoAY8BgRZ7PRKYk+tw8y0xV2gxNwC8ucs98r5wHt/19PgjCfdLh896hEW16MOo8GhEdMyWgvT/K+t6uc5FqnF9bnrjJh1WeIHfMDOzFyejuG5iQtfIvlF8Gk5Hf4vVB7RvdJ5hYT4NBkYxRs/YRkueaw+nr8htP9kyh7JrplzXgdtscFPVopMDZ4S4L6GHnVHQxOqz0TcPKG5lXjYCYOH5YxnxBrDw++gbcoMOUe/cl2RhSlxwpHReSTkgCpBXw991x6bIq+PhrNNYbR79HszkpGjt+YRNlrJk73aYrf1ThW3NRqU+UUlgQK6KylxsIgLnnISs4BjbYyABs1tstP8eOv8ef1LKHONtJSJ9xZBRkiRYbbR8r2GNhhJr9QPCVr8Dh5lFC46GsL14bnki/9sd/Jz9WrbuF3dkH0ngbSKMm3FWf/vgRfHv/2bPSSfRguRdmancr1mkzzpkb836J7I5XZJ/eW8w9sKbndIUHrN6KQsL3oP265uk/TohiMK15rir7BJppelzOO/48VmsIveIhDevQ/xnjVFFqvVRaOpkAQPzFXuA2hhN6tVH+D16tSAHa/9oeqk55jwkQzz6IUJLQdHNo4M+7usUWVPctSQyRF1bFOPdUXkUS5mVTWk6xBKKlmVrGS3qBVPxIsFYuj9N5zZ67ZDPwTPNIU1OMEMr24qc1ckzS1hoFtO+l4BQg2d/2KrLIf0EJKEIs3vICQ==","pineId":"PUB;2187","pineVersion":"-1","in_0":{"v":6,"f":true,"t":"integer"},"in_1":{"v":200,"f":true,"t":"integer"},"in_2":{"v":true,"f":true,"t":"bool"},"in_3":{"v":true,"f":true,"t":"bool"},"in_4":{"v":1,"f":true,"t":"integer"},"in_5":{"v":false,"f":true,"t":"bool"},"in_6":{"v":false,"f":true,"t":"bool"},"in_7":{"v":0,"f":true,"t":"integer"},"in_8":{"v":"fixed","f":true,"t":"text"},"in_9":{"v":1,"f":true,"t":"float"},"in_10":{"v":100000,"f":true,"t":"float"},"in_11":{"v":"NONE","f":true,"t":"text"},"in_12":{"v":0,"f":true,"t":"integer"},"in_13":{"v":"percent","f":true,"t":"text"},"in_14":{"v":0,"f":true,"t":"float"}}]}',
        '~m~52~m~{"m":"quote_create_session","p":["qs_FMJxhSRfoSKr"]}',
        '~m~98~m~{"m":"quote_add_symbols","p":["qs_FMJxhSRfoSKr","BITFINEX:BTCUSD",{"flags":["force_permission"]}]}',
        '~m~585~m~{"m":"create_study","p":["cs_zzchpGKpeP6K","st3","st1","s1","ESD@tv-scripting-101!",{"text":"VGcsD1b1BCal6jcB0hjOmA==_DVip081wb911Ia8CXJN9UsBVS7hWJgHTdDhHML6JtownD3znGWQq7+gm5NHZ0QsIWuSqQ9DL41FFX0thcPt65tkweQWRPSHnqYsOT8YZX5C8Nnru+BtePjbJpIGLnRE+eAmM4a3tSE7lDVMZjsy12CWQZSgMqThQOyihxVJlh3El5yNjTewDF+r+du3XLWijzTKyILhlMZdo8AsV8LlFTohnfSFwmlAQkCb+bp5jZ7tk87ScZiRgfsos0MXrv7hceG5lziad6qukoOcIJsxq9x/7Y9UwSMUS0m2s+r1j/7eHfjro7hYCPS5InsyreMniErjvNYs5HjgJgOA7gP1LvScauIW7u0FOHL3bbJ3vNGsiQtRjV7j8hM2pIs/AXSQhYUgbfhszpd8X8otQ/O+rOhygEIEZ+A2IpA==","pineId":"TV_EARNINGS","pineVersion":"2.0"}]}',
        '~m~507~m~{"m":"create_study","p":["cs_zzchpGKpeP6K","st4","st1","s1","ESD@tv-scripting-101!",{"text":"TeZXTQdPf3FuM7vXT2DGGA==_D++w0YvAUJYANfrcA56zC3S0XWU47+wMBdYwEL2m1wqmL+gTnQ9DeSEl5WLRJLOa9nYhtscIZgiI3SIKrhCf/MZ/UzIN/tXOfLVwTPwi92b/S0NhM+Hn3ZsLhWl7zniVIPvHNtYMXo+P5aU6QyWJWBO3LNYZoPYA9793K/eO6NfEFso+6f+96vuuxa5RQYoSkhJhoNBoFZUX2epR2KCOJxTVkJQTzerB7wTfnAC67UwVX7C4tUYWsGd4VlAzs1h+8igkcSmmQK2actAo2nsgCywEsZkA9nmtvuGHNly4P4K3MRCNRcX1Vu/UHsWB15BRd5xwfEPeJkFAcheMMR+mwIw=","pineId":"TV_SPLITS","pineVersion":"2.0"}]}',
        '~m~450~m~{"m":"create_study","p":["cs_zzchpGKpeP6K","st5","st1","s1","ESD@tv-scripting-101!",{"text":"gimxgnKhmHnYE+ANNOuzFQ==_juVkT8blafTfHghm5vEt9Yn8xgPr/LBADgXTquxe7DCci5lj3VvJiiTObidoHFnRe49OAxE9gQTWMg+Kd/YXXI+y2BKMI5bmPxp73fKJ5XtEE+4fx+4UBjKWJqS7mVjuH9bcwpg0+3oNR76wxnTi4RGVtBsyCfQtEB2Kw+O25A/YeeYIkG9WxrTTafBTZJAxG5YcwvMwjmLj3jmLrMzUNKj4WdCSRwXUziMA3nymfLQWPgDVkovqVfZ0ewNKrXFmUcopHyGzxpeEjRv+ypLeqjH2Kl8=","pineId":"TV_DIVIDENDS","pineVersion":"2.0"}]}',
        '~m~68~m~{"m":"quote_fast_symbols","p":["qs_FMJxhSRfoSKr","BITFINEX:BTCUSD"]}',
        '~m~62~m~{"m":"request_more_tickmarks","p":["cs_zzchpGKpeP6K","s1",10]}',
        '~m~58~m~{"m":"request_more_data","p":["cs_zzchpGKpeP6K","s1",871]}',
        '~m~40~m~{"m":"switch_protocol","p":["protobuf"]}',

    ]

    for idx, req in enumerate(reqs):
        print('send: ', idx)
        # req = write_msg(req)
        # print(req)
        # ws.send(json.dumps(req, ensure_ascii=False))
        ws.send(req)


if __name__ == "__main__":
    sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart%2FrP0mQCuj%2F&date=2018_12_13-11_47"
    headers = ["Accept-Encoding:gzip, deflate, br",
               "Accept-Language:zh-CN,zh;q=0.9",
               "Cache-Control:no-cache",
               "Connection:Upgrade",
               "Cookie:sessionid=8ekew6x1bmmuv6l5ohcsuvzhpw3rgivi; tv_ecuid=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; km_ni=bingpoli%40gmail.com; km_lv=x; km_ai=bingpoli%40gmail.com; __utmz=226258911.1544029652.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.1603730878.1543933608; __utmc=226258911; __utma=226258911.1603730878.1543933608.1544806780.1544806780.33; _sp_ses.cf1a=*; _sp_id.cf1a=97499503-6490-448e-a43c-e11e5ceef0ec.1543933609.10.1544876814.1544806780.95b8b338-b7fc-45d7-adb5-0ed968c0c345; __utmt=1; kvcd=1544876815474; km_vs=1; __utmb=226258911.15.9.1544876876895",
               "Host:data.tradingview.com",
               "Origin:https://cn.tradingview.com",
               "Pragma:no-cache",
               "Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits",
               "Sec-WebSocket-Key:Gv9G0W4+ivVatfkBsORnRQ==",
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
