#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.main.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.FxPro.MT5.main.py - Ver.0.0.4 Update:2020.12.23" |
#//+------------------------------------------------------------------+
#//|                                   PyCharm : PlugIn - AWS ToolKit |
#//|                               https://aws.amazon.com/jp/pycharm/ |
#//+------------------------------------------------------------------+
import json
import os

import MetaTrader5 as mt5
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


### Demo.Session : Setup ###
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

## MT5.Session : ShutDown
mt5.shutdown()
