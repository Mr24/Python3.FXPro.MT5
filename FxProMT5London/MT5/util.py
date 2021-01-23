#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.util.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.FxPro.MT5.util.py - Ver.0.1.2 Update:2021.01.23" |
#//+------------------------------------------------------------------+
import logging
from datetime import datetime

import MetaTrader5 as mt5
import dateutil.parser
import pandas as pd
import pytz


logger = logging.getLogger(__name__)

class Balance(object):
    def __init__(self, currency, available):
        self.currency = currency
        self.available = available

class Ticker(object):
    def __init__(self, product_code, timestamp, bid, ask, volume):
    # def __init__(self, product_code, timestamp, bid, ask):
    # def __init__(self, Ticks_From):
    # def __init__(self, timestamp, bid, ask):
        # self.Ticks_From = Ticks_From
        self.product_code = product_code
        self.timestamp = timestamp
        self.bid = bid
        self.ask = ask
        self.volume = volume

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

        ## TimeZone : Setup
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1500)

        ## TimeZone : UTC.Setup
        timezone = pytz.timezone("Etc/UTC")
        utc_from = datetime(2021, 1, 22, tzinfo=timezone)

        ticks_from = mt5.copy_ticks_from(Product_Code, utc_from, 100000, mt5.COPY_TICKS_ALL)
        # ticks_from = mt5.copy_ticks_from("USDJPY", utc_from, 100000, mt5.COPY_TICKS_ALL)

        # count = 0
        # for tick in ticks_from:
        #    count += 1
            # print(tick)
        #    if count > 10:
        #        break

        # (Unix.Time)
        timestamp = ticks_from['time']
        # (DateTime)
        # ticks_frame = pd.DataFrame(ticks_from)
        # ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
        # timestamp = ticks_frame['time']
        bid = ticks_from['bid']
        # bid = float(ticks_from['bid'])
        ask = ticks_from['ask']
        volume = ticks_from['volume']

        # return ticks_from
        # return Ticker(ticks_from)
        return Ticker(Product_Code, timestamp, bid, ask, volume)

