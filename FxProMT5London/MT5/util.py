#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.util.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.FxPro.MT5.util.py - Ver.0.1.2.1 Update:2021.01.24" |
#//+------------------------------------------------------------------+
import logging

import MetaTrader5 as mt5


logger = logging.getLogger(__name__)

class Balance(object):
    def __init__(self, currency, available):
        self.currency = currency
        self.available = available

class Ticker(object):
    def __init__(self, product_code, timestamp, bid, ask, volume):
        self.product_code = product_code
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask
        self.volume = volume
        # self.all = all


class MT5Client(object):
    def __init__(self, ID, PW, FxServer):
        self.ID = ID
        self.PW = PW
        self.client = mt5.initialize(login=ID, password=PW, server=FxServer)

    def get_balance(self):
        account_info_dict = mt5.account_info()._asdict()
        available = account_info_dict['balance']
        currency = account_info_dict['currency']
        return Balance(currency, available)

    def get_ticker(self, Product_Code):
        symbol_info_tick = mt5.symbol_info_tick(Product_Code)._asdict()
        timestamp = symbol_info_tick['time_msc']
        bid = symbol_info_tick['bid']
        ask = symbol_info_tick['ask']
        volume = symbol_info_tick['volume_real']
        '''
        all = list()
        all = all.addend(bid)
        all = all.addend(ask)
        return Ticker(bid, ask, all)
        '''
        return Ticker(Product_Code, timestamp, bid, ask, volume)

