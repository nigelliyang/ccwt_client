#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/15 0:41 By xycfree
# @Descript:  https://blog.csdn.net/CSDN_Boring/article/details/77542644
# https://www.cnblogs.com/JetpropelledSnake/p/9033064.html
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

    req = '{"id":1569439,"channel":"chat","text":{"content":{"data":{"id":"0bf2ba63-1128-463c-af8e-5cb23f977332","is_pro_limited":false,"user_id":137744,"time":"Fri Dec 21 06:22:05 2018 UTC","is_pro":false,"pro_plan":"","interval":"60","top_user_info":null,"text":"@usu mrng bro","symbol":"OANDA:XAUUSD","meta":{"links":{},"text":"","version":"0.2","interval":"60"},"room_id":"spKNkcfKuFVnvOKV","is_moderator":false,"type":"","username":"gongal","user_pic":"https:\/\/s3.tradingview.com\/userpics\/137744-d1fs_mid.png","is_staff":false},"action":"message"},"channel":"chat_spKNkcfKuFVnvOKV"}}'

    # req = json.dumps(req, ensure_ascii=False)
    # _req = '~m~' + str(len(req)) + '~m~' + req
    ws.send(req)
    # req1 = {"e": "quote_set_fields", "t":{"fields": ["ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume"],
    #                                       "session": "qs_ykbzkG8oM4Vx"}}
    # ws.send(req1)
    #
    # req2 = {"e": "quote_add_symbols", "t": {"session": "qs_ykbzkG8oM4Vx", "symbols": ["BITFINEX:BTCUSD",{"flags":["force_permission"]}]}}
    # ws.send(req2)







if __name__ == "__main__":
    sock_adress = "wss://pushstream.tradingview.com/message-pipe-ws/public/chat"

    headers = ["Accept-Encoding:gzip, deflate, br",
               "Accept-Language:zh-CN,zh;q=0.9",
               "Cache-Control:no-cache",
               "Connection:Upgrade",
               "Cookie:__utmc=226258911; __utmz=226258911.1545115285.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sessionid=tyhmsgs2l4helf8gu9tta2liszjwf72l; png=cef7e9b2-2ce7-4382-b898-51f6c723782d; etg=cef7e9b2-2ce7-4382-b898-51f6c723782d; cachec=cef7e9b2-2ce7-4382-b898-51f6c723782d; tv_ecuid=cef7e9b2-2ce7-4382-b898-51f6c723782d; km_ni=bingpoli%40gmail.com; _sp_id.cf1a=0a6c336e-2d8c-4f64-b8a7-79a482634e04.1545115285.1.1545115384.1545115285.bd0db8ff-65e6-4b77-8d15-118446f89f07; kvcd=1545115384608; km_ai=bingpoli%40gmail.com; km_lv=1545115385; __utmd=1; __utma=226258911.812481980.1545115285.1545115285.1545115384.2; __utmb=226258911.2.9.1545120262532",
               "Host:data.tradingview.com",
               "Origin:https://cn.tradingview.com",
               "Pragma:no-cache",
               "Sec-WebSocket-Extensions:permessage-deflate; client_max_window_bits",
               "Sec-WebSocket-Key:yBVHo7rV1NVD55abaQDIkQ==",
               "Sec-WebSocket-Version:13",
               "Upgrade:websocket",
               "User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
               ]
    websocket.enableTrace(True)
    # websocket.enableTrace(False)

    ws = websocket.WebSocketApp(sock_adress, header=headers,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_timeout=30)
