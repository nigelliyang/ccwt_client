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
        '~m~55~m~{"m":"chart_create_session","p":["cs_kllUhspHvjaI",""]}',
        '~m~52~m~{"m":"quote_create_session","p":["qs_mAUENNLl7vbD"]}',
        '~m~268~m~{"m":"quote_set_fields","p":["qs_mAUENNLl7vbD","ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume"]}',
        '~m~98~m~{"m":"quote_add_symbols","p":["qs_mAUENNLl7vbD","BITFINEX:BTCUSD",{"flags":["force_permission"]}]}',
        '~m~68~m~{"m":"quote_fast_symbols","p":["qs_mAUENNLl7vbD","BITFINEX:BTCUSD"]}',
        '~m~63~m~{"m":"switch_timezone","p":["cs_kllUhspHvjaI","Asia/Shanghai"]}',
        '~m~119~m~{"m":"resolve_symbol","p":["cs_kllUhspHvjaI","symbol_1","={\"symbol\":\"BITFINEX:BTCUSD\",\"adjustment\":\"splits\"}"]}',
        '~m~75~m~{"m":"create_series","p":["cs_kllUhspHvjaI","s1","s1","symbol_1","45",300]}',
        '~m~126~m~{"m":"create_study","p":["cs_kllUhspHvjaI","st1","st1","s1","Volume@tv-basicstudies-81",{"length":20,"col_prev_close":false}]}',
        '~m~2112~m~{"m":"create_study","p":["cs_kllUhspHvjaI","st2","st1","s1","StrategyScript@tv-scripting-101!",{"text":"2sMXFZEjEcAEL0TdZuTIQA==_Ms0NAfB4PBEpsMEJL29vRZnweB9M0oyj4eO625LXy1/T6EnFjvZPYvO5V7QS+6mdXgxFthk3XpTftMC3l23+JkK6NWfL1g13DydoA5L7gSC/Vi3LAFTxx8QJMWo/u4rLgfdiZDJC1o/JWj6J0iBXmk3XiVdZroPx0NDoGSNzORqMQziSTldq7Nt/4bJB5NBzuBrtCbWd7j66GAOnTRJB7vG4SGWbkFqOv4wRbFAoOkSoMyC1/6ZeflXdWcyZGk0YPsxpcp9JOOU4dEgnHHXI+sZCCjuIv5IK+lmtwnXPhlPRyiRpqQjUDOHMQZqlO4vlmqgOuxKDeJ57tyFGaiIIuIChwStgOg4CN24pCf0SMy8wEW4rax1Y/MvlHb9qQ9HpS18ka1nGdbrGc3UHFQ25kudgsPE9wC4KiZVXSCarniMhyV6tTXt+boAH8g8U4BPaSSCNAr+lh2WNYHl/ddZJ9JaZWod/VIlPo732Ili2DZg1neeIK3O3TMTKMROB5THzE6yQnrE5GrVxY2h291GSdjt5a04ayWwpzZizvGG/e4Pug/8UWsydpjifVmhwF7purE3EdNDrXxG56uKu8Xh3RZF5A68HFcIzpXYSyefNxcfN0MsTfHnoAY8BgRZ7PRKYk+tw8y0xV2gxNwC8ucs98r5wHt/19PgjCfdLh896hEW16MOo8GhEdMyWgvT/K+t6uc5FqnF9bnrjJh1WeIHfMDOzFyejuG5iQtfIvlF8Gk5Hf4vVB7RvdJ5hYT4NBkYxRs/YRkueaw+nr8htP9kyh7JrplzXgdtscFPVopMDZ4S4L6GHnVHQxOqz0TcPKG5lXjYCYOH5YxnxBrDw++gbcoMOUe/cl2RhSlxwpHReSTkgCpBXw991x6bIq+PhrNNYbR79HszkpGjt+YRNlrJk73aYrf1ThW3NRqU+UUlgQK6KylxsIgLnnISs4BjbYyABs1tstP8eOv8ef1LKHONtJSJ9xZBRkiRYbbR8r2GNhhJr9QPCVr8Dh5lFC46GsL14bnki/9sd/Jz9WrbuF3dkH0ngbSKMm3FWf/vgRfHv/2bPSSfRguRdmancr1mkzzpkb836J7I5XZJ/eW8w9sKbndIUHrN6KQsL3oP265uk/TohiMK15rir7BJppelzOO/48VmsIveIhDevQ/xnjVFFqvVRaOpkAQPzFXuA2hhN6tVH+D16tSAHa/9oeqk55jwkQzz6IUJLQdHNo4M+7usUWVPctSQyRF1bFOPdUXkUS5mVTWk6xBKKlmVrGS3qBVPxIsFYuj9N5zZ67ZDPwTPNIU1OMEMr24qc1ckzS1hoFtO+l4BQg2d/2KrLIf0EJKEIs3vICQ==","pineId":"PUB;2187","pineVersion":"-1","in_0":{"v":6,"f":true,"t":"integer"},"in_1":{"v":200,"f":true,"t":"integer"},"in_2":{"v":true,"f":true,"t":"bool"},"in_3":{"v":true,"f":true,"t":"bool"},"in_4":{"v":1,"f":true,"t":"integer"},"in_5":{"v":false,"f":true,"t":"bool"},"in_6":{"v":false,"f":true,"t":"bool"},"in_7":{"v":0,"f":true,"t":"integer"},"in_8":{"v":"fixed","f":true,"t":"text"},"in_9":{"v":1,"f":true,"t":"float"},"in_10":{"v":100000,"f":true,"t":"float"},"in_11":{"v":"NONE","f":true,"t":"text"},"in_12":{"v":0,"f":true,"t":"integer"},"in_13":{"v":"percent","f":true,"t":"text"},"in_14":{"v":0,"f":true,"t":"float"}}]}',
        '~m~52~m~{"m":"quote_create_session","p":["qs_3yEykZfVsOQz"]}',
        '~m~98~m~{"m":"quote_add_symbols","p":["qs_3yEykZfVsOQz","BITFINEX:BTCUSD",{"flags":["force_permission"]}]}',
        '~m~62~m~{"m":"request_more_tickmarks","p":["cs_kllUhspHvjaI","s1",10]}',
        '~m~58~m~{"m":"request_more_data","p":["cs_kllUhspHvjaI","s1",338]}',
        '~m~450~m~{"m":"create_study","p":["cs_kllUhspHvjaI","st3","st1","s1","ESD@tv-scripting-101!",{"text":"NImxTSBSY+PYqDuxDvaesw==_oNNZ2M4DJDKIpe5hWBlHJOAD2nqEYNYqmz0QVf3u3Pb6th6LGFD9ZzPS4+RWy+lRSonn98Q2+27VQAzbS18JBUAUptbMxtvshOTIHKNvfTDYCWYyPOCddMQdFjdtQGVEoOFgeAV68hLTYoEn7jt2WP/VohynzVH6SZ476n0e9T/ZEjDOn7SMi9A/WfB7aATRzwG38H5RaZ/bhs3E1BTeRe8L6pH318dD/jqh7MvKIs9tpDI9uZW1WIvHbOvMMJ4TEnguyB9mLVruk+KZuHzq+7S+25M=","pineId":"TV_DIVIDENDS","pineVersion":"2.0"}]}',
        '~m~585~m~{"m":"create_study","p":["cs_kllUhspHvjaI","st4","st1","s1","ESD@tv-scripting-101!",{"text":"qCHdnTdJlJvjvPt2sGcClQ==_vpFR6KrumBxa6dy1AflFGIbl4aHMuIkSJZPs27NL/9nEJYI6kfCbZWHLXjbqS/3v8mC1748xrJ527r0itRk7VGuMJgvQnOwr+hq1MxqJMlXSYSvSQYvbGWZROLu1QJDKl4BXslMQAcBeI3qDjq0UMLZ4gpdAW0QqaSbjCg/sGJyQPoUuTdum+rcR0hrTVtao7l5nOjzhDRXPy5wDwuu9A/kFagVwctM6VzzkTnOvbbfPPH/AgY4LEgVaVb+qPwRMNMZ9vCuE6ljDu+qMhI4eKfcQ6+GrRewu68flAXjhyjgNwZAv9O/E1+HwSXvAmVAm62dPsinAbCORx5csJJLUsX/tnamBjLlp08N2fcZ3PgoeAEDd8aypmEkEPI8QgVKHuNJCwrDwmgEQ4HRlihsB2ZkdScJpj+W4dw==","pineId":"TV_EARNINGS","pineVersion":"2.0"}]}',
        '~m~507~m~{"m":"create_study","p":["cs_kllUhspHvjaI","st5","st1","s1","ESD@tv-scripting-101!",{"text":"HQM6bD9GM9enNDg+Dpbr5Q==_6mo59JGel13HFsJb4+zVLMIo4uclh698vg7jPokk/tb0/W+bSFLPdnXAjmEfmLWAr1M/qnj5pozLFHH1fDbitxdyejMXHOp8qlUTESUtCRXbul/7M1nBJziUgLYSeOlBGxDLgRXYofQbHfrWwv7X/PYf7nU7akbK4KetC0tDudASK06aXpWhQGD4rvvvhQdwIRlDlY5zAHJ2UpqWuY12ZW9fMTQbCjsd7Hpox0YNQAWdGXYf/BO3+7/QAK/Zxi+s/CVNdE2qo6LAzStiQzcNQPxT6UJ1LftVwR4rGBtpIMG59n79dsi7hXLOyK3ksRGpGZoYHtG96W98UR+qRzlS8FY=","pineId":"TV_SPLITS","pineVersion":"2.0"}]}',
        '~m~68~m~{"m":"quote_fast_symbols","p":["qs_3yEykZfVsOQz","BITFINEX:BTCUSD"]}',
        '~m~57~m~{"m":"request_more_data","p":["cs_kllUhspHvjaI","s1",27]}',
        '~m~40~m~{"m":"switch_protocol","p":["protobuf"]}'
    ]

    for idx, req in enumerate(reqs):
        print('send: ', idx)
        # req = write_msg(req)
        # print(req)
        # ws.send(json.dumps(req, ensure_ascii=False))
        ws.send(req)


if __name__ == "__main__":
    sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart%2FrP0mQCuj%2F&date=2018_12_18-13_13"
    cookie = "__utmc=226258911; __utmz=226258911.1545273193.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sessionid=hlmwt7p6rq6n9hwlprs9evhy61qist4l; cachec=undefined; etg=undefined; km_ni=bingpoli%40gmail.com; km_ai=bingpoli%40gmail.com; km_lv=x; _sp_ses.cf1a=*; km_vs=1; __utma=226258911.1361885574.1545273193.1545279384.1545285783.4; __utmt=1; _sp_id.cf1a=525edd29-fcb4-4ec7-bfb7-ad818db89660.1545273193.4.1545288293.1545281747.8a5590d1-8cc4-47bd-8ef0-9e83eb9d983d; kvcd=1545288293893; __utmb=226258911.58.1.1545288294975"
    socket_key = "m3TyFV0OnFlomon/Sn8LuQ=="

    headers = ["Accept-Encoding:gzip, deflate, br",
               "Accept-Language:zh-CN,zh;q=0.9",
               "Cache-Control:no-cache",
               "Connection:Upgrade",
               "Cookie:{}".format(cookie),
               "Host:data.tradingview.com",
               "Origin:https://cn.tradingview.com",
               "Pragma:no-cache",
               "Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits",
               "Sec-WebSocket-Key:{}".format(socket_key),
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
