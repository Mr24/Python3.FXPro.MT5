#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.main.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Py3.FxPro.MT5.settion.py - Ver.0.0.2 Update:2020.12.23" |
#//+------------------------------------------------------------------+
import json


### JSON.Load : fxpro_config.json ###
with open("FxPro/fxpro_config.json", encoding='utf-8') as f:
    fxpro_dict = json.load(f)

### Demo.Settion : Setup ###
DemoID = fxpro_dict['DemoID']
DemoPW = fxpro_dict['DemoPassword']
FxServer = fxpro_dict['FxProServer']

### Live. Settion : Setup ###
# LiveID = fxpro_dict['LiveID']
# LivePW = fxpro_dict['LivePassword']
