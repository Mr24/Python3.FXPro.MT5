#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.FXPro.MT5.Constants.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.FxPro.MT5.Constants.py - Ver.0.1.3 Update:2021.01.25" |
#//+------------------------------------------------------------------+
### FxProMT5London : Setup ###
DURATION_1M = '1M'
DURATION_1H = '1H'
DURATIONS = [DURATION_1M, DURATION_1H]

### MT5 : Setup ###
GRANULARITY_1M = 'TIMEFRAME_M1'
GRANULARITY_1H = 'TIMEFRAME_H1'

### Trade_Map ###
TRADE_MAP = {
    DURATION_1M: {
        'duration': DURATION_1M,
        'granularity': GRANULARITY_1M,
    },
    DURATION_1H: {
        'duration': DURATION_1H,
        'granularity': GRANULARITY_1H,
    }
}
