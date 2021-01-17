#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.util.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.FxPro.MT5.util.py - Ver.0.1.1 Update:2021.01.14" |
#//+------------------------------------------------------------------+
import logging

import MetaTrader5 as mt5


logger = logging.getLogger(__name__)

class Balance(object):
    def __init__(self, currency, available):
        self.currency = currency
        self.available = available

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
