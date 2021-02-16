#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.main.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.FxPro.MT5.main.py - Ver.0.1.7 Update:2021.02.16" |
#//+------------------------------------------------------------------+
#//|                                   PyCharm : PlugIn - AWS ToolKit |
#//|                               https://aws.amazon.com/jp/pycharm/ |
#//+------------------------------------------------------------------+
#//|                                           khramkov/MQL5-JSON-API |
#//|                        https://github.com/khramkov/MQL5-JSON-API |
#//+------------------------------------------------------------------+
import json
import pandas as pd

import MetaTrader5 as mt5
import FxPro.session as fxproSession
from MT5.util import MT5Client
from MT5 import util

import threading
import time


### MT5.Demo : Default.Setup ###
if __name__ == "__main__":
    ## MT5.Session : Setup
    mt5_cli = MT5Client(fxproSession.DemoID, fxproSession.DemoPW, fxproSession.FxServer)
    if not mt5_cli:
        print("initialize() failed")
        mt5.shutdown

    ## MT5.Session : Accont_Info
    Balance = mt5_cli.get_balance()
    print(Balance.currency, Balance.available)

    ## MT5.Session : Symbol_Info_Tick
    Ticker = mt5_cli.get_ticker("USDJPY")
    print(Ticker.product_code, Ticker.timestamp, Ticker.bid, Ticker.ask, Ticker.volume)
    print(Ticker.truncate_date_time('1M'))
    print(Ticker.truncate_date_time('1H'))
    print(Ticker.mid_price)

    Ticker.re_tick("USDJPY")

    # mt5_cli.thread_ticker()
    # mt5_cli.thread_ticker()
    # t = threading.Thread(target=mt5_cli.thread_ticker, args="")
    # t.start()

    # tTick = mt5_cli.thread_ticker("USDJPY")
    # print(tTick.product_code, tTick.timestamp, tTick.bid, tTick.ask, tTick.volume)

    # print(Ticker.stream_tick)
    # print(util._t_livedata())
    # (Ver.0.1.6-OK) Ticker.stream_tick()

### MT5.Demo.Session : Setup ###
# DemoID = fxproSession.DemoID
# DemoPW = fxproSession.DemoPW
# FxServer = fxproSession.FxServer

## MT5.Session : Setup
# if not mt5.initialize(login=DemoID, password=DemoPW, server=FxServer):
#    print("initialize() failed")
#    mt5.shutdown()

## MT5.Session : Accont_Info
# account_info_dict = mt5.account_info()._asdict()
# available = account_info_dict['balance']
# currency = account_info_dict['currency']
# print(currency, available)
## df = pd.DataFrame(list(account_info_dict.items()), columns = ['property', 'value'])
## print(df)

## MT5.Session : Terminal_Info
# print(mt5.terminal_info())
## MT5.Session : Version
# print(mt5.version())

## MT5.Session : ShutDown
mt5.shutdown()