#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/6 0:17 By xycfree
# @Descript:
import json
import re
import struct
import websocket

# 设置交易所及交易对，70行处需要手动修改交易所及交易对，BITFINEX:BTCUSD
exchange_symbol = "BITFINEX:BTCUSD"


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
    message = message.decode('utf-8') if isinstance(message, bytes) else message
    print("接收数据: {}".format(message))
    if len(message) < 20:
        pass
    else:
        mess = re.sub(r'~m~\d+~m~', '', message)
        try:
            mess = json.loads(mess)
        except Exception as e:
            print(e)

        print(mess)
        with open('rsa_double.txt', mode='a+', encoding='utf-8') as f:
            f.write(mess)
            f.write('\n')


def on_error(ws, error):
    # 程序报错时，就会触发on_error事件
    print("异常错误: {}".format(error))


def on_close(ws):
    print("Connection closed ……")


def on_open(ws):
    # 连接到服务器之后就会触发on_open事件，这里用于send数据
    print('on_open')
    reqs = [
        json.dumps({"m":"chart_create_session","p":["cs_yD7aPrM9Eav2",""]}),
        json.dumps({"m":"quote_create_session","p":["qs_CiWdgz2rquIv"]}),
        json.dumps({"m":"quote_set_fields","p":["qs_CiWdgz2rquIv","ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume"]}),
        json.dumps({"m":"quote_add_symbols","p":["qs_CiWdgz2rquIv",exchange_symbol,{"flags":["force_permission"]}]}),
        json.dumps({"m":"quote_fast_symbols","p":["qs_CiWdgz2rquIv",exchange_symbol]}),
        json.dumps({"m":"switch_timezone","p":["cs_yD7aPrM9Eav2","Asia/Shanghai"]}),
        # 以下一行的交易对 BITFINEX:BTCUSD，需要修改；
        '{"m":"resolve_symbol","p":["cs_yD7aPrM9Eav2","symbol_1","={\\"symbol\\":\\"BITFINEX:BTCUSD\\",\\"adjustment\\":\\"splits\\"}"]}',

        json.dumps({"m":"create_series","p":["cs_yD7aPrM9Eav2","s1","s1","symbol_1","45",300]}),
        json.dumps({"m":"create_study","p":["cs_yD7aPrM9Eav2","st1","st1","s1","Volume@tv-basicstudies-81",{"length":20,"col_prev_close":False}]}),
        json.dumps({"m":"create_study","p":["cs_yD7aPrM9Eav2","st2","st1","s1","StrategyScript@tv-scripting-101!",{"text":"2sMXFZEjEcAEL0TdZuTIQA==_Ms0NAfB4PBEpsMEJL29vRZnweB9M0oyj4eO625LXy1/T6EnFjvZPYvO5V7QS+6mdXgxFthk3XpTftMC3l23+JkK6NWfL1g13DydoA5L7gSC/Vi3LAFTxx8QJMWo/u4rLgfdiZDJC1o/JWj6J0iBXmk3XiVdZroPx0NDoGSNzORqMQziSTldq7Nt/4bJB5NBzuBrtCbWd7j66GAOnTRJB7vG4SGWbkFqOv4wRbFAoOkSoMyC1/6ZeflXdWcyZGk0YPsxpcp9JOOU4dEgnHHXI+sZCCjuIv5IK+lmtwnXPhlPRyiRpqQjUDOHMQZqlO4vlmqgOuxKDeJ57tyFGaiIIuIChwStgOg4CN24pCf0SMy8wEW4rax1Y/MvlHb9qQ9HpS18ka1nGdbrGc3UHFQ25kudgsPE9wC4KiZVXSCarniMhyV6tTXt+boAH8g8U4BPaSSCNAr+lh2WNYHl/ddZJ9JaZWod/VIlPo732Ili2DZg1neeIK3O3TMTKMROB5THzE6yQnrE5GrVxY2h291GSdjt5a04ayWwpzZizvGG/e4Pug/8UWsydpjifVmhwF7purE3EdNDrXxG56uKu8Xh3RZF5A68HFcIzpXYSyefNxcfN0MsTfHnoAY8BgRZ7PRKYk+tw8y0xV2gxNwC8ucs98r5wHt/19PgjCfdLh896hEW16MOo8GhEdMyWgvT/K+t6uc5FqnF9bnrjJh1WeIHfMDOzFyejuG5iQtfIvlF8Gk5Hf4vVB7RvdJ5hYT4NBkYxRs/YRkueaw+nr8htP9kyh7JrplzXgdtscFPVopMDZ4S4L6GHnVHQxOqz0TcPKG5lXjYCYOH5YxnxBrDw++gbcoMOUe/cl2RhSlxwpHReSTkgCpBXw991x6bIq+PhrNNYbR79HszkpGjt+YRNlrJk73aYrf1ThW3NRqU+UUlgQK6KylxsIgLnnISs4BjbYyABs1tstP8eOv8ef1LKHONtJSJ9xZBRkiRYbbR8r2GNhhJr9QPCVr8Dh5lFC46GsL14bnki/9sd/Jz9WrbuF3dkH0ngbSKMm3FWf/vgRfHv/2bPSSfRguRdmancr1mkzzpkb836J7I5XZJ/eW8w9sKbndIUHrN6KQsL3oP265uk/TohiMK15rir7BJppelzOO/48VmsIveIhDevQ/xnjVFFqvVRaOpkAQPzFXuA2hhN6tVH+D16tSAHa/9oeqk55jwkQzz6IUJLQdHNo4M+7usUWVPctSQyRF1bFOPdUXkUS5mVTWk6xBKKlmVrGS3qBVPxIsFYuj9N5zZ67ZDPwTPNIU1OMEMr24qc1ckzS1hoFtO+l4BQg2d/2KrLIf0EJKEIs3vICQ==","pineId":"PUB;2187","pineVersion":"-1","in_0":{"v":6,"f":True,"t":"integer"},"in_1":{"v":200,"f":True,"t":"integer"},"in_2":{"v":True,"f":True,"t":"bool"},"in_3":{"v":True,"f":True,"t":"bool"},"in_4":{"v":1,"f":True,"t":"integer"},"in_5":{"v":False,"f":True,"t":"bool"},"in_6":{"v":False,"f":True,"t":"bool"},"in_7":{"v":0,"f":True,"t":"integer"},"in_8":{"v":"fixed","f":True,"t":"text"},"in_9":{"v":1,"f":True,"t":"float"},"in_10":{"v":100000,"f":True,"t":"float"},"in_11":{"v":"NONE","f":True,"t":"text"},"in_12":{"v":0,"f":True,"t":"integer"},"in_13":{"v":"percent","f":True,"t":"text"},"in_14":{"v":0,"f":True,"t":"float"}}]}),
        json.dumps({"m":"create_study","p":["cs_yD7aPrM9Eav2","st3","st1","s1","RSI@tv-basicstudies-81",{"length":14,"source":"close"}]}),


        # '{"m":"quote_create_session","p":["qs_cYic7cSheeMW"]}',
        # '{"m":"quote_add_symbols","p":["qs_cYic7cSheeMW","BITFINEX:BTCUSD",{"flags":["force_permission"]}]}',
        # '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st4","st1","s1","ESD@tv-scripting-101!",{"text":"WGl55Gc/tbDhxqE0Sd3ToA==_YMmxzJDP/iyAhzIO4g0ZJKV6ytpyksGXDXR08MYNKe8xzjywJ+tCoD4k0gmsAqFZlb/B/DJ3ky1VfawnRN/8ZTPt+j0G7XoEPBAXVDpMtOyn2NdaIqgbIpholgHJ1xItlSv4nZHTzLqC40eWypnCbn+LpNydbAFHpYICB96gIAnMsFmuRD3VGQAUTnygHsaT9rN78lA3i+PR86C1ditNUWFhROycV6VFGdBCTENuR2wLQGQvzC9634qEFDoMvcqGyqCUvU00O+CnBD2tT9a55CQq1pw=","pineId":"TV_DIVIDENDS","pineVersion":"2.0"}]}',
        # '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st5","st1","s1","ESD@tv-scripting-101!",{"text":"sfKNX/tKLjp7L7FtVgmYXg==_z+3RKkf/RqO+wVT0vRe9xjdf+jQNDEzfVUnKgAJ8UIQVc8CtKEeU3OYuwetrsoJGUQbQO6hKOm2aL2r3D2XmjaKB9UoLV7DR/3ly5ab8iU+cTEBFh+7DAgcr7mOnQ99tTXt31jQA/AZ27rof8Kq0Hi6MRcGfyvAQiba9bDnKSKiXnCj4HpV/MaLaG/6vieOqFg6a429ZzD3p9hIX2oEIXpIJjHpWwe8csyz0K9AUjiC5y/bu2E0Rek7UVwBVDS7pMOJXEJcJNOPlFdRDiGcvUKgJJERtCxq1gNu+hkHYIVthDa7FUIxoepryRSRlwvKqMumeGvOWUlMewHHJWKWBLRwim9jyVRRrwQ5vYNF6k9lwZ0rAaKNIqpnLgZP4lkOLzafcnjvGOp9/rk1XTaQkVZwbBNvakKegKQ==","pineId":"TV_EARNINGS","pineVersion":"2.0"}]}',
        # '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st6","st1","s1","ESD@tv-scripting-101!",{"text":"trOzbbylgCYupam1bHdZXA==_EaZ3Cmxj0Rcu994IpoTzq1hz0of0vj3v9QrqeWWETpqXANkwIRiBufkSTlvEGZe2lUTfotOkiMkpGiDFtPmKgbKyhmNn1bsPm5KMCgWf+WVhyM06LKhpm84grDwUBMOrauaxZ9kBy7TIRibaf/S3ov2god437NRrOGMaFl1wBPApJK7LrJi1Uh3P71rShB+o1W0TIZ2/Tp+2sVg6Kt3Ker/OnlZKMbbIMA2hz4AbTgiRue6RhsuLzF9j1SgILzi1vC1AXIIWleVmzMIQeap+s3pJQvnW8dB3J3fE0VkCH6+y+S5z37wk4AaNH/Ki7UqWeAitpEedZ9HX5QTpC+6fa/s=","pineId":"TV_SPLITS","pineVersion":"2.0"}]}',
        # '{"m":"request_more_tickmarks","p":["cs_yD7aPrM9Eav2","s1",10]}',
        # '{"m":"request_more_data","p":["cs_yD7aPrM9Eav2","s1",162]}',
        # '{"m":"quote_fast_symbols","p":["qs_cYic7cSheeMW","BITFINEX:BTCUSD"]}',
        # '{"m":"switch_protocol","p":["protobuf"]}',
    ]


    # reqs = [
    #     '{"m":"chart_create_session","p":["cs_yD7aPrM9Eav2",""]}',
    #     '{"m":"quote_create_session","p":["qs_CiWdgz2rquIv"]}',
    #     '{"m":"quote_set_fields","p":["qs_CiWdgz2rquIv","ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume"]}',
    #     '{"m":"quote_add_symbols","p":["qs_CiWdgz2rquIv","BITFINEX:BTCUSD",{"flags":["force_permission"]}]}',
    #     '{"m":"quote_fast_symbols","p":["qs_CiWdgz2rquIv","BITFINEX:BTCUSD"]}',
    #     '{"m":"switch_timezone","p":["cs_yD7aPrM9Eav2","Asia/Shanghai"]}',
    #     '{"m":"resolve_symbol","p":["cs_yD7aPrM9Eav2","symbol_1","={\\"symbol\\":\\"BITFINEX:BTCUSD\\",\\"adjustment\\":\\"splits\\"}"]}',
    #     '{"m":"create_series","p":["cs_yD7aPrM9Eav2","s1","s1","symbol_1","45",300]}',
    #     '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st1","st1","s1","Volume@tv-basicstudies-81",{"length":20,"col_prev_close":False}]}',
    #     '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st2","st1","s1","StrategyScript@tv-scripting-101!",{"text":"2sMXFZEjEcAEL0TdZuTIQA==_Ms0NAfB4PBEpsMEJL29vRZnweB9M0oyj4eO625LXy1/T6EnFjvZPYvO5V7QS+6mdXgxFthk3XpTftMC3l23+JkK6NWfL1g13DydoA5L7gSC/Vi3LAFTxx8QJMWo/u4rLgfdiZDJC1o/JWj6J0iBXmk3XiVdZroPx0NDoGSNzORqMQziSTldq7Nt/4bJB5NBzuBrtCbWd7j66GAOnTRJB7vG4SGWbkFqOv4wRbFAoOkSoMyC1/6ZeflXdWcyZGk0YPsxpcp9JOOU4dEgnHHXI+sZCCjuIv5IK+lmtwnXPhlPRyiRpqQjUDOHMQZqlO4vlmqgOuxKDeJ57tyFGaiIIuIChwStgOg4CN24pCf0SMy8wEW4rax1Y/MvlHb9qQ9HpS18ka1nGdbrGc3UHFQ25kudgsPE9wC4KiZVXSCarniMhyV6tTXt+boAH8g8U4BPaSSCNAr+lh2WNYHl/ddZJ9JaZWod/VIlPo732Ili2DZg1neeIK3O3TMTKMROB5THzE6yQnrE5GrVxY2h291GSdjt5a04ayWwpzZizvGG/e4Pug/8UWsydpjifVmhwF7purE3EdNDrXxG56uKu8Xh3RZF5A68HFcIzpXYSyefNxcfN0MsTfHnoAY8BgRZ7PRKYk+tw8y0xV2gxNwC8ucs98r5wHt/19PgjCfdLh896hEW16MOo8GhEdMyWgvT/K+t6uc5FqnF9bnrjJh1WeIHfMDOzFyejuG5iQtfIvlF8Gk5Hf4vVB7RvdJ5hYT4NBkYxRs/YRkueaw+nr8htP9kyh7JrplzXgdtscFPVopMDZ4S4L6GHnVHQxOqz0TcPKG5lXjYCYOH5YxnxBrDw++gbcoMOUe/cl2RhSlxwpHReSTkgCpBXw991x6bIq+PhrNNYbR79HszkpGjt+YRNlrJk73aYrf1ThW3NRqU+UUlgQK6KylxsIgLnnISs4BjbYyABs1tstP8eOv8ef1LKHONtJSJ9xZBRkiRYbbR8r2GNhhJr9QPCVr8Dh5lFC46GsL14bnki/9sd/Jz9WrbuF3dkH0ngbSKMm3FWf/vgRfHv/2bPSSfRguRdmancr1mkzzpkb836J7I5XZJ/eW8w9sKbndIUHrN6KQsL3oP265uk/TohiMK15rir7BJppelzOO/48VmsIveIhDevQ/xnjVFFqvVRaOpkAQPzFXuA2hhN6tVH+D16tSAHa/9oeqk55jwkQzz6IUJLQdHNo4M+7usUWVPctSQyRF1bFOPdUXkUS5mVTWk6xBKKlmVrGS3qBVPxIsFYuj9N5zZ67ZDPwTPNIU1OMEMr24qc1ckzS1hoFtO+l4BQg2d/2KrLIf0EJKEIs3vICQ==","pineId":"PUB;2187","pineVersion":"-1","in_0":{"v":6,"f":True,"t":"integer"},"in_1":{"v":200,"f":True,"t":"integer"},"in_2":{"v":True,"f":True,"t":"bool"},"in_3":{"v":True,"f":True,"t":"bool"},"in_4":{"v":1,"f":True,"t":"integer"},"in_5":{"v":False,"f":True,"t":"bool"},"in_6":{"v":False,"f":True,"t":"bool"},"in_7":{"v":0,"f":True,"t":"integer"},"in_8":{"v":"fixed","f":True,"t":"text"},"in_9":{"v":1,"f":True,"t":"float"},"in_10":{"v":100000,"f":True,"t":"float"},"in_11":{"v":"NONE","f":True,"t":"text"},"in_12":{"v":0,"f":True,"t":"integer"},"in_13":{"v":"percent","f":True,"t":"text"},"in_14":{"v":0,"f":True,"t":"float"}}]}',
    #     '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st3","st1","s1","RSI@tv-basicstudies-81",{"length":14,"source":"close"}]}',
    #
    #     # '{"m":"quote_create_session","p":["qs_cYic7cSheeMW"]}',
    #     # '{"m":"quote_add_symbols","p":["qs_cYic7cSheeMW","BITFINEX:BTCUSD",{"flags":["force_permission"]}]}',
    #     # '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st4","st1","s1","ESD@tv-scripting-101!",{"text":"WGl55Gc/tbDhxqE0Sd3ToA==_YMmxzJDP/iyAhzIO4g0ZJKV6ytpyksGXDXR08MYNKe8xzjywJ+tCoD4k0gmsAqFZlb/B/DJ3ky1VfawnRN/8ZTPt+j0G7XoEPBAXVDpMtOyn2NdaIqgbIpholgHJ1xItlSv4nZHTzLqC40eWypnCbn+LpNydbAFHpYICB96gIAnMsFmuRD3VGQAUTnygHsaT9rN78lA3i+PR86C1ditNUWFhROycV6VFGdBCTENuR2wLQGQvzC9634qEFDoMvcqGyqCUvU00O+CnBD2tT9a55CQq1pw=","pineId":"TV_DIVIDENDS","pineVersion":"2.0"}]}',
    #     # '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st5","st1","s1","ESD@tv-scripting-101!",{"text":"sfKNX/tKLjp7L7FtVgmYXg==_z+3RKkf/RqO+wVT0vRe9xjdf+jQNDEzfVUnKgAJ8UIQVc8CtKEeU3OYuwetrsoJGUQbQO6hKOm2aL2r3D2XmjaKB9UoLV7DR/3ly5ab8iU+cTEBFh+7DAgcr7mOnQ99tTXt31jQA/AZ27rof8Kq0Hi6MRcGfyvAQiba9bDnKSKiXnCj4HpV/MaLaG/6vieOqFg6a429ZzD3p9hIX2oEIXpIJjHpWwe8csyz0K9AUjiC5y/bu2E0Rek7UVwBVDS7pMOJXEJcJNOPlFdRDiGcvUKgJJERtCxq1gNu+hkHYIVthDa7FUIxoepryRSRlwvKqMumeGvOWUlMewHHJWKWBLRwim9jyVRRrwQ5vYNF6k9lwZ0rAaKNIqpnLgZP4lkOLzafcnjvGOp9/rk1XTaQkVZwbBNvakKegKQ==","pineId":"TV_EARNINGS","pineVersion":"2.0"}]}',
    #     # '{"m":"create_study","p":["cs_yD7aPrM9Eav2","st6","st1","s1","ESD@tv-scripting-101!",{"text":"trOzbbylgCYupam1bHdZXA==_EaZ3Cmxj0Rcu994IpoTzq1hz0of0vj3v9QrqeWWETpqXANkwIRiBufkSTlvEGZe2lUTfotOkiMkpGiDFtPmKgbKyhmNn1bsPm5KMCgWf+WVhyM06LKhpm84grDwUBMOrauaxZ9kBy7TIRibaf/S3ov2god437NRrOGMaFl1wBPApJK7LrJi1Uh3P71rShB+o1W0TIZ2/Tp+2sVg6Kt3Ker/OnlZKMbbIMA2hz4AbTgiRue6RhsuLzF9j1SgILzi1vC1AXIIWleVmzMIQeap+s3pJQvnW8dB3J3fE0VkCH6+y+S5z37wk4AaNH/Ki7UqWeAitpEedZ9HX5QTpC+6fa/s=","pineId":"TV_SPLITS","pineVersion":"2.0"}]}',
    #     # '{"m":"request_more_tickmarks","p":["cs_yD7aPrM9Eav2","s1",10]}',
    #     # '{"m":"request_more_data","p":["cs_yD7aPrM9Eav2","s1",162]}',
    #     # '{"m":"quote_fast_symbols","p":["qs_cYic7cSheeMW","BITFINEX:BTCUSD"]}',
    #     # '{"m":"switch_protocol","p":["protobuf"]}',
    # ]

    for req in reqs:
        # _req = json.dumps(req, ensure_ascii=False)
        _req = req
        # send_req = req
        _req_len = len(_req)
        send_req = '~m~' + str(_req_len) + '~m~' + _req
        # print('发送: {}'.format(send_req))
        ws.send(send_req)



if __name__ == "__main__":
    sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart%2FrP0mQCuj%2F&date=2018_12_20-19_52"
    cookie = "__utmc=226258911; __utmz=226258911.1545358476.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); km_lv=x; sessionid=8togr3m4llxfq1megba6bfduhzo9ky2q; png=cef7e9b2-2ce7-4382-b898-51f6c723782d; etg=cef7e9b2-2ce7-4382-b898-51f6c723782d; cachec=cef7e9b2-2ce7-4382-b898-51f6c723782d; tv_ecuid=cef7e9b2-2ce7-4382-b898-51f6c723782d; km_ni=bingpoli%40gmail.com; km_ai=bingpoli%40gmail.com; __utma=226258911.196369246.1545358476.1545360446.1545373147.3; _sp_id.cf1a=a25b6ccb-1c8e-4770-9efc-c4f2e23548cb.1545358476.3.1545375560.1545360776.1a8655b8-295a-4f4b-8e9a-062d84370d48; kvcd=1545375560495"
    socket_key = "IKCDm3xUHYihgLkjnobp5A=="

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
