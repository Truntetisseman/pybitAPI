import json
from pybit import usdt_perpetual
from pybit.usdt_perpetual import HTTP
import datetime
import time


# CONFIG
mode = "test"
timeframe = 60
kline_limit = 200
z_score_window = 2
api_url = "https://api-testnet.bybit.com" if mode == "test" else "https://api.bybit.com"

# SESSION Activation
session = HTTP(
    endpoint="https://api-testnet.bybit.com")

time_start_date = 0
if timeframe == 60:
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
if timeframe == "D":
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)
time_start_seconds = int(time_start_date.timestamp())


def get_tradeable_symbols():

    # Get available symbols
    sym_list = []
    symbols = session.query_symbol()
    if "ret_msg" in symbols.keys():
        if symbols["ret_msg"] == "OK":
            symbols = symbols["result"]
            for symbol in symbols:
                if symbol["quote_currency"] == "USDT" and float(symbol["maker_fee"]) > 0 and symbol["status"] == "Trading":
                    sym_list.append(symbol)
    print(sym_list)
    print(len(sym_list))
                    
    # Return ouput
    return sym_list
# Get historical prices (klines)
def get_price_klines(symbol):

    # Get prices
    prices = session.query_mark_price_kline(
        symbol = symbol,
        interval = timeframe,
        limit = kline_limit,
        from_time = time_start_seconds
    )

    # Manage API calls
    time.sleep(0.1)

    # Return output
    if len(prices["result"]) != kline_limit:
        return []
    print(prices["result"])
    return prices["result"]

# Store price histry for all available pairs
def store_price_history(symbols):
    # Get prices and store in DataFrame
    counts = 0
    price_history_dict = {}
    for sym in symbols:
        symbol_name = sym["name"]
        price_history = get_price_klines(symbol_name)
        if len(price_history) > 0:
            price_history_dict[symbol_name] = price_history
            counts += 1
            print(f"{counts} items stored")
        else:
            print(f"{counts} items not stored")

    # Output prices to JSON
    if len(price_history_dict) > 0:
        with open("1_price_list.json", "w") as fp:
            json.dump(price_history_dict, fp, indent=4)
        print("Prices saved successfully.")

    # Return output
    return



get_tradeable_symbols()