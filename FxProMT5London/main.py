#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.main.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.FxPro.MT5.main.py - Ver.0.0.5 Update:2021.01.13" |
#//+------------------------------------------------------------------+
#//|                                   PyCharm : PlugIn - AWS ToolKit |
#//|                               https://aws.amazon.com/jp/pycharm/ |
#//+------------------------------------------------------------------+
import json
import os

import MetaTrader5 as mt5
from datetime import datetime

import boto3 as b3
import mysql.connector as mConn

import FxPro.session as fxproSession
import AWS.mysql as rdsSession


### AWS.MySQL.Session : Setup ###
ENDPOINT = rdsSession.ENDPOINT
PORT = rdsSession.PORT
USR = rdsSession.USR
PW = rdsSession.PW
REGION = rdsSession.REGION
DBNAME = rdsSession.DBNAME
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

## AWS.MySQL.Session : Get Token ###
rds_session = b3.Session(profile_name='default')
rds_client = b3.client('rds')
# (Get.Token) rds_token = rds_client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)


## AWS.MySQL.DB : Connect ###
try:
    conn = mConn.connect(host=ENDPOINT, user=USR, passwd=PW, port=PORT, database=DBNAME)
    # (Get.Token) conn = mConn.connect(host=ENDPOINT, user=USR, passwd=rds_token, port=PORT, database=DBNAME)
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)

except Exception as e:
    print("Database connection failed due to {}".format(e))


### MT5.Demo.Session : Setup ###
DemoID = fxproSession.DemoID
DemoPW = fxproSession.DemoPW
FxServer = fxproSession.FxServer

## MT5.Session : Setup
if not mt5.initialize(login=DemoID, password=DemoPW, server=FxServer):
    print("initialize() failed")
    mt5.shutdown()

## MT5.Session : Info
print(mt5.terminal_info())
## MT5.Session : Version
print(mt5.version())


### MT5.Ticks : USDJPY - 1000
usdjpy_ticks = mt5.copy_ticks_from("USDJPY", datetime(2020,12,23,9), 1000, mt5.COPY_TICKS_ALL)
usdjpy_rates = mt5.copy_rates_from("USDJPY", mt5.TIMEFRAME_M1, datetime(2020,12,23,9), 1000)


## MT5.Session : ShutDown
mt5.shutdown()


# print('usdjpy_ticks(', len(usdjpy_ticks), ')')
# for val in usdjpy_ticks[:10]: print(val)

print('usdjpy_rates(', len(usdjpy_rates), ')')
for val in usdjpy_rates[:10]: print(val)
