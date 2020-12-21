#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.main.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.FxPro.MT5.main.py - Ver.0.0.1 Update:2020.12.22" |
#//+------------------------------------------------------------------+
import json

import MetaTrader5 as mt5

with open("fxpro_config.json", encoding='utf-8') as f:
    fxpro_dict = json.load(f)

DemoID = fxpro_dict['DemoID']
DemoPW = fxpro_dict['DemoPassword']
FxServer = fxpro_dict['FxProServer']

if not mt5.initialize(login=DemoID, password=DemoPW, server=FxServer):
    print("initialize() failed")
    mt5.shutdown()

print(mt5.terminal_info())

print(mt5.version())

mt5.shutdown()
