#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.util.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.FxPro.MT5.util.py - Ver.0.1.4 Update:2021.01.25" |
#//+------------------------------------------------------------------+
import logging
from datetime import datetime
import dateutil.parser

import MetaTrader5 as mt5
import MT5.constants as MT5Cons


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

    @property
    def time(self):
        return datetime.utcfromtimestamp(self.timestamp)

    def truncate_date_time(self, duration):
        ticker_time = self.time
        # (Now) 2021-01-25 10:11:12
        # (1M)  2021-01-25 10:11:00
        # (1H)  2021-01-25 10:00:00
        if duration == MT5Cons.DURATION_1M:
            time_format = '%Y-%m-%d %H:%M'
        elif duration == MT5Cons.DURATION_1H:
            time_format = '%Y-%m-%d %H'
        else:
            logger.warning('action=truncate_date_time error=no_datetime_format')
            return None

        str_date = datetime.strftime(ticker_time, time_format)
        return datetime.strptime(str_date, time_format)

    @property
    def mid_price(self):
        return (self.bid + self.ask) / 2


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
        timestamp = symbol_info_tick['time']
        # timestamp = symbol_info_tick['time_msc']
        bid = symbol_info_tick['bid']
        ask = symbol_info_tick['ask']
        volume = self.get_candle_volume(Product_Code, "1M", 1)
        # volume = symbol_info_tick['volume_real']
        '''
        all = list()
        all = all.addend(bid)
        all = all.addend(ask)
        return Ticker(bid, ask, all)
        '''
        return Ticker(Product_Code, timestamp, bid, ask, volume)

    def get_candle_volume(self, Product_Code, granularity, count):
        granularity_code = MT5Cons.TRADE_MAP[granularity]['granularity']
        copy_rates_from_pos = mt5.copy_rates_from_pos(Product_Code, granularity_code, 0, count)
        # copy_rates_from_pos = mt5.copy_rates_from_pos(Product_Code, mt5.TIMEFRAME_M1, 0, 1)
        volume = copy_rates_from_pos['tick_volume']
        return volume
