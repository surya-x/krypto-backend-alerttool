import json
import threading
import time
import api_key
import send
from config import *
import SQL_CRUD
from binance import Client
from pprint import pformat
from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager

TEST_API_KEY = api_key.TEST_API_KEY
TEST_API_SECRET = api_key.TEST_API_SECRET
base_endpoint = 'https://api.binance.com'

lc_symbols = {'BNBBUSD': [], 'BTCBUSD': [], 'ETHBUSD': [], 'LTCBUSD': [], 'TRXBUSD': [],
              'XRPBUSD': [], 'BNBUSDT': [], 'BTCUSDT': [], 'ETHUSDT': [], 'LTCUSDT': [],
              'TRXUSDT': [], 'XRPUSDT': [], 'BNBBTC': [], 'ETHBTC': [], 'LTCBTC': [],
              'TRXBTC': [], 'XRPBTC': [], 'LTCBNB': [], 'TRXBNB': [], 'XRPBNB': []}


def handle_price_change(symbol, timestamp, price):
    print(f"Handle price change for symbol: {symbol}, timestamp: {timestamp}, price: {price}")
    global lc_symbols
    if symbol in lc_symbols:
        # print(lc_symbols[symbol])
        for each in lc_symbols[sybol]:
            # print(each)
            if each[0] == float(price):
                print("Target reached for alert_id {}".format(each[1]))
                send.main(str(each[1]))


def process_stream_data(binance_websocket_api_manager):
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_data = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        is_empty = is_empty_message(oldest_data)
        if is_empty:
            time.sleep(0.01)
        else:
            oldest_data_dict = json.loads(oldest_data)
            data = oldest_data_dict['data']
            #  Handle price change
            handle_price_change(symbol=data['s'], timestamp=data['T'], price=data['p'])


def start_websocket_listener():
    binance_us_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
    channels = {'trade', }
    binance_us_websocket_api_manager.create_stream(channels, markets=symbols, api_key=TEST_API_KEY,
                                                   api_secret=TEST_API_SECRET)

    print("staring worker thread")
    # Start a worker process to move the received stream_data from the stream_buffer to a print function
    worker_thread = threading.Thread(target=process_stream_data, args=(binance_us_websocket_api_manager,))
    worker_thread.start()


def is_empty_message(message):
    if message is False:
        return True
    if '"result":null' in message:
        return True
    if '"result":None' in message:
        return True
    return False


def compare_server_times(client):
    server_time = client.get_server_time()
    aa = str(server_time)
    bb = aa.replace("{'serverTime': ", "")
    aa = bb.replace("}", "")
    gg = int(aa)
    ff = gg - 10799260
    uu = ff / 1000
    yy = int(uu)
    tt = time.localtime(yy)
    print(f"Binance Server time: {tt}")
    print(f"Local time: {time.localtime()}")


def get_traded_symbols(client):
    symbols = []
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
        symbols.append(s['symbol'])
    return symbols


def get_exchange_info(client):
    info = client.get_exchange_info()
    print(pformat(info))
    tickers = client.get_all_tickers()
    print(pformat(tickers))


def push_to_lc(sym: str, trigger: float, alert_id: int):
    global lc_symbols
    if sym in lc_symbols:
        lc_symbols[sym].append((trigger, alert_id))
    else:
        temp_list = [(trigger, alert_id)]
        lc_symbols[sym] = temp_list

    print(lc_symbols)


if __name__ == "__main__":
    #  Define symbols
    symbols = ['BNBBUSD', 'BTCBUSD', 'ETHBUSD', 'LTCBUSD', 'TRXBUSD',
               'XRPBUSD', 'BNBUSDT', 'BTCUSDT', 'ETHUSDT', 'LTCUSDT',
               'TRXUSDT', 'XRPUSDT', 'BNBBTC', 'ETHBTC', 'LTCBTC',
               'TRXBTC', 'XRPBTC', 'LTCBNB', 'TRXBNB', 'XRPBNB']

    # symbols = ['BTCBUSD']

    # lc_symbols = {}
    table = SQL_CRUD.SQL_CRUD(user=user,
                              password=password,
                              host=host,
                              port=port,
                              dbname=database,
                              table=alerts_table)
    table.connect()
    selected = table.get_all_alerts()
    table.commit()
    # print(selected)
    for each in selected:
        if each[1] in lc_symbols:
            if each[3] == 'CREATED':
                myt = (each[2], each[0])
                lc_symbols[each[1]].append(myt)

    print(lc_symbols)
    #  Initialize binance client
    client = Client(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET, testnet=True)

    # #  Compare server and local times
    compare_server_times(client)

    # #  Get traded symbols
    # traded_symbols = get_traded_symbols(client)
    # print("Traded symbols: ", traded_symbols)

    start_websocket_listener()
