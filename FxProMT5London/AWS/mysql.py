#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.main.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|       "VsV.Py3.FxPro.MT5.mysql.py - Ver.0.0.5 Update:2021.01.13" |
#//+------------------------------------------------------------------+
import json


### JSON.Load : fxpro_config.json ###
with open("AWS/aws_config.json", encoding='utf-8') as f:
    rds_dict = json.load(f)


### AWS.RDS.MySQL : Setup ###
ENDPOINT = rds_dict['host'] 	# AWS.RDS.MySQL : EndPoint
PORT = rds_dict['port']			# AWS.RDS.MySQL : Port
USR = rds_dict['user']			# AWS.RDS.MySQL : UserName
PW = rds_dict['password']		# AWS.RDS.MySQL : PassWord
REGION = rds_dict['region']		# AWS.RDS.MySQL : Region
DBNAME = rds_dict['database']	# AWS.RDS.MySQL : Database Name