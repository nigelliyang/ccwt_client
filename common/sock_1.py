#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/12/5 23:54 By xycfree
# @Descript:

from ws4py.client.threadedclient import WebSocketClient


class CG_Client(WebSocketClient):
    def opened(self):
        req = '~m~66~m~{"m":"depth_set_symbol","p":["ds_CdR5HlOGgka1","BITFINEX:BTCUSD"]}'
        self.send(req)
        pass

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        # resp = json.loads(str(resp))
        # data = resp['data']
        # if type(data) is dict:
        #     ask = data['asks'][0]
        #     print('Ask:', ask)
        #     bid = data['bids'][0]
        #     print('Bid:', bid)
        print(resp)


if __name__ == '__main__':
    sock_adress = "wss://data.tradingview.com/socket.io/websocket?from=chart%2FrP0mQCuj%2F&date=2018_12_13-11_47"
    ws = None
    try:
        ws = CG_Client(sock_adress, headers=[
            ("Accept-Encoding", "gzip, deflate, br"),
            ("Accept-Language", "zh-CN,zh;q=0.9"),
            ("Cache-Control", "no-cache"),
            ("Connection", "Upgrade"),
            ("Cookie",
             "sessionid=8ekew6x1bmmuv6l5ohcsuvzhpw3rgivi; tv_ecuid=b118b0fa-cf0e-4d3b-bd90-cba970230cd4; km_ni=bingpoli%40gmail.com; km_lv=x; km_ai=bingpoli%40gmail.com; __utmz=226258911.1544029652.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.1603730878.1543933608; __utma=226258911.1603730878.1543933608.1544196238.1544196238.24; __utmc=226258911; __utmt=1; _sp_ses.cf1a=*; km_vs=1; _sp_id.cf1a=97499503-6490-448e-a43c-e11e5ceef0ec.1543933609.8.1544713475.1544196238.eb1bd66e-ef1b-4689-a64c-6293ecaa168f; kvcd=1544713474809; __utmb=226258911.15.9.1544713538190"),
            ("Host", "data.tradingview.com"),
            ("Origin", "https://cn.tradingview.com"),
            ("Pragma", "no-cache"),
            ("Sec-WebSocket-Extensions", "permessage-deflate; client_max_window_bits"),
            ("Sec-WebSocket-Key", "CsSSefIwhq6mYFASYsZb3A=="),
            ("Sec-WebSocket-Version", "13"),
            ("Upgrade", "websocket"),
            ("User-Agent",
             "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"),
        ]
                       )
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
