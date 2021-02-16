#//+------------------------------------------------------------------+
#//|                           VerysVeryInc.Python3.FXPro.MT5.util.py |
#//|                  Copyright(c) 2020, VerysVery Inc. & Yoshio.Mr24 |
#//|                       https://github.com/Mr24/Python3.FXPro.MT5/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.FxPro.MT5.util.py - Ver.0.1.7 Update:2021.02.16" |
#//+------------------------------------------------------------------+
#//|                                           khramkov/MQL5-JSON-API |
#//|                        https://github.com/khramkov/MQL5-JSON-API |
#//+------------------------------------------------------------------+
#//|                                           Python/Threading.Timer |
#//|                    https://ja.stackoverflow.com/questions/24508/ |
#//+------------------------------------------------------------------+
import logging
from datetime import datetime
import dateutil.parser

import MetaTrader5 as mt5
import MT5.constants as MT5Cons

import zmq
import threading
import time
from threading import Timer


logger = logging.getLogger(__name__)

### ZeroMQ : Setup ###
class MTraderAPI:
    def __init__(self, host=None):
        self.HOST = host or 'localhost'
        self.SYS_PORT = 15555  # REP/REQ port
        self.DATA_PORT = 15556  # PUSH/PULL port
        self.LIVE_PORT = 15557  # PUSH/PULL port
        self.EVENTS_PORT = 15558  # PUSH/PULL port
        self.INDICATOR_DATA_PORT = 15559  # REP/REQ port
        self.CHART_DATA_PORT = 15560  # PUSH port

        # ZeroMQ timeout in seconds
        sys_timeout = 1
        data_timeout = 10

        # sys_timeout = 1
        # data_timeout = 10

        # initialise ZMQ context
        context = zmq.Context()

        # connect to server sockets
        try:
            self.sys_socket = context.socket(zmq.REQ)
            # set port timeout
            self.sys_socket.RCVTIMEO = sys_timeout * 1000
            self.sys_socket.connect('tcp://{}:{}'.format(self.HOST, self.SYS_PORT))

            self.data_socket = context.socket(zmq.PULL)
            # set port timeout
            self.data_socket.RCVTIMEO = data_timeout * 1000
            self.data_socket.connect('tcp://{}:{}'.format(self.HOST, self.DATA_PORT))

            self.indicator_data_socket = context.socket(zmq.PULL)
            # set port timeout
            self.indicator_data_socket.RCVTIMEO = data_timeout * 1000
            self.indicator_data_socket.connect(
                "tcp://{}:{}".format(self.HOST, self.INDICATOR_DATA_PORT)
            )
            self.chart_data_socket = context.socket(zmq.PUSH)
            # set port timeout
            # TODO check if port is listening and error handling
            self.chart_data_socket.connect(
                "tcp://{}:{}".format(self.HOST, self.CHART_DATA_PORT)
            )

        except zmq.ZMQError:
            raise zmq.ZMQBindError("Binding ports ERROR")

    def _send_request(self, data: dict) -> None:
        """Send request to server via ZeroMQ System socket"""
        try:
            self.sys_socket.send_json(data)
            msg = self.sys_socket.recv_string()
            # terminal received the request
            assert msg == 'OK', 'Something wrong on server side'
        except AssertionError as err:
            raise zmq.NotDone(err)
        except zmq.ZMQError:
            raise zmq.NotDone("Sending request ERROR")

    def _pull_reply(self):
        """Get reply from server via Data socket with timeout"""
        try:
            msg = self.data_socket.recv_json()
        except zmq.ZMQError:
            raise zmq.NotDone('Data socket timeout ERROR')
        return msg

    def _indicator_pull_reply(self):
        """Get reply from server via Data socket with timeout"""
        try:
            msg = self.indicator_data_socket.recv_json()
        except zmq.ZMQError:
            raise zmq.NotDone("Indicator Data socket timeout ERROR")
        if self.debug:
            print("ZMQ INDICATOR DATA REPLY: ", msg)
        return msg

    def live_socket(self, context=None):
        """Connect to socket in a ZMQ context"""
        try:
            context = context or zmq.Context.instance()
            socket = context.socket(zmq.PULL)
            socket.connect('tcp://{}:{}'.format(self.HOST, self.LIVE_PORT))
        except zmq.ZMQError:
            raise zmq.ZMQBindError("Live port connection ERROR")
        return socket

    def streaming_socket(self, context=None):
        """Connect to socket in a ZMQ context"""
        try:
            context = context or zmq.Context.instance()
            socket = context.socket(zmq.PULL)
            socket.connect('tcp://{}:{}'.format(self.HOST, self.EVENTS_PORT))
        except zmq.ZMQError:
            raise zmq.ZMQBindError("Data port connection ERROR")
        return socket

    def _push_chart_data(self, data: dict) -> None:
        """Send message for chart control to server via ZeroMQ chart data socket"""
        try:
            if self.debug:
                print("ZMQ PUSH CHART DATA: ", data, " -> ", data)
            self.chart_data_socket.send_json(data)
        except zmq.ZMQError:
            raise zmq.NotDone("Sending request ERROR")

    def construct_and_send(self, **kwargs) -> dict:
        """Construct a request dictionary from default and send it to server"""

        # default dictionary
        request = {
            "action": None,
            "actionType": None,
            "symbol": None,
            "chartTF": None,
            "fromDate": None,
            "toDate": None,
            "id": None,
            "magic": None,
            "volume": None,
            "price": None,
            "stoploss": None,
            "takeprofit": None,
            "expiration": None,
            "deviation": None,
            "comment": None,
            "chartId": None,
            "indicatorChartId": None,
            "chartIndicatorSubWindow": None,
            "style": None,
        }

        # update dict values if exist
        for key, value in kwargs.items():
            if key in request:
                request[key] = value
            else:
                raise KeyError('Unknown key in **kwargs ERROR')

        # send dict to server
        self._send_request(request)

        # return server reply
        return self._pull_reply()

    def indicator_construct_and_send(self, **kwargs) -> dict:
        """Construct a request dictionary from default and send it to server"""

        # default dictionary
        request = {
            "action": None,
            "actionType": None,
            "id": None,
            "symbol": None,
            "chartTF": None,
            "fromDate": None,
            "toDate": None,
            "name": None,
            "params": None,
            "linecount": None,
        }

        # update dict values if exist
        for key, value in kwargs.items():
            if key in request:
                request[key] = value
            else:
                raise KeyError("Unknown key in **kwargs ERROR")

        # send dict to server
        self._send_request(request)

        # return server reply
        return self._indicator_pull_reply()

    def chart_data_construct_and_send(self, **kwargs) -> dict:
        """Construct a request dictionary from default and send it to server"""

        # default dictionary
        message = {
            "action": None,
            "actionType": None,
            "chartId": None,
            "indicatorChartId": None,
            "data": None,
        }

        # update dict values if exist
        for key, value in kwargs.items():
            if key in message:
                message[key] = value
            else:
                raise KeyError("Unknown key in **kwargs ERROR")

        # send dict to server
        self._push_chart_data(message)


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

    @property
    def stream_tick(self):

        t = threading.Thread(target=_t_livedata, daemon=True)
        t.start()

        t = threading.Thread(target=_t_streaming_events, daemon=True)
        t.start()

        while True:
            pass

        # api = MTraderAPI()
        # rep = api.construct_and_send(action="ACCOUNT")
        # rep = api.construct_and_send(action="CONFIG", symbol="USDJPY", chartTF="M1")
        # rep = api.construct_and_send(action="HISTORY", actionType="DATA", symbol="USDJPY", chartTF="M5", fromDate="1612557509")
        # rep = api.construct_and_send(action="CONFIG", symbol="USDJPY", chartTF="TICK")
        # rep = api.construct_and_send(action="RESET")

        # return rep


    def re_tick(self, Product_Code):
        t = RepeatedTimer(0.0001, _t_ticker, [Product_Code])
        t.start()
        # time.sleep(0.01)
        # t.cancel()

        while True:
            pass

        # now = time.time()
        # t = threading.Timer(1, _t_ticker)
        # t = threading.Thread(target=_t_ticker(), daemon=True)
        # t.start()
        # t.join()
        # wait_time = time_interval - ( (time.time() - now) % time_interval)
        # time.sleep(wait_time)


class RepeatedTimer(Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        Timer.__init__(self, interval, self.run, args, kwargs)
        self.thread = None
        self.function = function

    def run(self):
        self.thread = Timer(self.interval, self.run)
        self.thread.start()
        self.function(*self.args, **self.kwargs)

    def cancel(self):
        if self.thread is not None:
            self.thread.cancel()
            self.thread.join()
            del self.thread


def _t_livedata():
    api = MTraderAPI()
    socket = api.live_socket()
    while True:
        try:
            last_candle = socket.recv_json()
        except zmq.ZMQError:
            raise zmq.NotDone("Live data ERROR")
        print(last_candle)
        # return last_candle

def _t_streaming_events():
    api = MTraderAPI()
    socket = api.streaming_socket()
    while True:
        try:
            trans = socket.recv_json()
            request, reply = trans.values()
        except zmq.ZMQError:
            raise zmq.NotDone("Streaming data ERROR")
        print(request)
        print(reply)
        # return request, reply

def _t_ticker(Product_Code):
    symbol_info_tick = mt5.symbol_info_tick(Product_Code)._asdict()
    # symbol_info_tick = mt5.symbol_info_tick('USDJPY')._asdict()
    timestamp = symbol_info_tick['time']
    bid = symbol_info_tick['bid']
    ask = symbol_info_tick['ask']

    print(Product_Code, timestamp, bid, ask)
    # print('USDJPY', timestamp, bid, ask)
    # print(symble, timestamp, bid, ask)


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
